/* global marked, DOMPurify, hljs, chrome */
(() => {
  'use strict';

  // Dropbox's file viewer (the full-page preview and the quick-view panel in
  // the file list) shows the file inside PREVIEW_CONTENT. Markdown files have
  // two modes there: plain text (TEXT_PREVIEW) and Dropbox's own rendering.
  const TEXT_PREVIEW = '[data-testid="fvsdk_text_preview"]';
  const PREVIEW_CONTENT = '[data-testid="fvsdk_preview_content"]';
  const QUICKVIEW_TITLE = '[data-testid="quick-view-titlebar-test-id"]';
  const MD_EXT = /\.(md|markdown|mdown|mkd|mkdn|mdx)$/i;
  // The viewer loads the original file from previews.dropbox.com/p/orig/<token>/p.<ext>
  const ORIG_URL = /^https:\/\/previews\.dropbox\.com\/p\/orig\//;
  const ORIG_MD = /\/p\.(md|markdown|mdown|mkd|mkdn|mdx)(\?|$)/i;

  // Most recent last. Dropbox also prefetches neighbouring files, so the
  // newest URL is not necessarily the file on screen.
  const origUrls = [];

  // A PerformanceObserver keeps receiving entries even after the page's
  // resource timing buffer is full, so we never miss a newly opened file.
  try {
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        if (!ORIG_URL.test(e.name)) continue;
        const i = origUrls.indexOf(e.name);
        if (i !== -1) origUrls.splice(i, 1);
        origUrls.push(e.name);
        if (origUrls.length > 20) origUrls.shift();
        schedule(); // the file on screen may be the one that just loaded
      }
    }).observe({ type: 'resource', buffered: true });
  } catch (_) {
    // Fall back to reading the DOM only.
  }

  const cssPromise = Promise.all(
    ['lib/github-markdown.css', 'lib/hljs-github.min.css', 'lib/hljs-github-dark.min.css', 'preview.css'].map((p) =>
      fetch(chrome.runtime.getURL(p)).then((r) => r.text())
    )
  ).then(([gh, hlLight, hlDark, own]) => {
    const css = [
      gh,
      `@media (prefers-color-scheme: light) { ${hlLight} }`,
      `@media (prefers-color-scheme: dark) { ${hlDark} }`,
      own,
    ].join('\n');
    // Dropbox has its own light/dark setting, independent of the OS, so build
    // a fixed light and a fixed dark variant; 'auto' follows the OS.
    const fixed = (scheme) =>
      css.replace(/@media \(prefers-color-scheme: (dark|light)\)/g, (_, s) =>
        s === scheme ? '@media all' : '@media not all'
      );
    return { auto: css, light: fixed('light'), dark: fixed('dark') };
  }).catch(() => ({ auto: '', light: '', dark: '' }));

  // Dropbox marks its theme on <html>: dig-Mode--bright or dig-Mode--dark.
  function dropboxScheme() {
    const c = document.documentElement.className;
    if (/\bdig-Mode--dark\b/.test(c)) return 'dark';
    if (/\bdig-Mode--(bright|light)\b/.test(c)) return 'light';
    return 'auto';
  }

  const sheetCache = {};

  async function applyTheme(root) {
    const scheme = dropboxScheme();
    const css = (await cssPromise)[scheme];
    try {
      if (!sheetCache[scheme]) {
        sheetCache[scheme] = new CSSStyleSheet();
        sheetCache[scheme].replaceSync(css);
      }
      root.adoptedStyleSheets = [sheetCache[scheme]];
    } catch (_) {
      let style = root.querySelector('style');
      if (!style) root.prepend((style = document.createElement('style')));
      style.textContent = css;
    }
  }

  function isMarkdownFile() {
    if (MD_EXT.test(decodeURIComponent(location.pathname))) return true;
    // Full-page preview: /home/<folder>?preview=<file>.md
    if (MD_EXT.test(new URLSearchParams(location.search).get('preview') || '')) return true;
    if (origUrls.length && ORIG_MD.test(origUrls[origUrls.length - 1])) return true;
    // Quick-view title bar reads e.g. "00_總表MD • 6.71 KB"
    const qv = document.querySelector(QUICKVIEW_TITLE);
    return !!qv && /(MD|MARKDOWN|MDX)\s*•/.test(qv.textContent);
  }

  // Make sure the fetched file is the one Dropbox is showing (the last preview
  // URL could belong to a previously opened or prefetched file). Only letters
  // and digits are compared, because Dropbox's rendered text has no Markdown
  // syntax such as ** or |.
  function sameFile(source, renderedText) {
    const norm = (s) => s.replace(/[^\p{L}\p{N}]+/gu, '');
    const probe = renderedText.split('\n').map(norm).filter((l) => l.length >= 4).slice(0, 8);
    if (!probe.length) return false;
    const body = norm(source);
    const hits = probe.filter((l) => body.includes(l)).length;
    return hits >= Math.ceil(probe.length * 0.6);
  }

  const sources = new Map(); // preview URL -> file text

  async function fetchSource(url) {
    if (!sources.has(url)) {
      const r = await fetch(url, { credentials: 'include' });
      if (!r.ok) return null;
      sources.set(url, await r.text());
    }
    return sources.get(url);
  }

  // Returns the Markdown source of the file Dropbox is showing, or null.
  async function findSource(renderedText) {
    const candidates = origUrls.filter((u) => ORIG_MD.test(u)).reverse().slice(0, 5);
    for (const url of candidates) {
      try {
        const text = await fetchSource(url);
        if (text !== null && sameFile(text, renderedText)) return text;
      } catch (_) {
        // Try the next candidate.
      }
    }
    return null;
  }

  function stripFrontMatter(md) {
    return md.replace(/^\uFEFF?---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
  }

  function render(md, overlay) {
    const html = marked.parse(stripFrontMatter(md), { gfm: true, breaks: false });
    overlay.innerHTML = DOMPurify.sanitize(html, { ADD_ATTR: ['target'] });
    overlay.querySelectorAll('pre code').forEach((el) => {
      try {
        hljs.highlightElement(el);
      } catch (_) {
        // Leave the block unhighlighted.
      }
    });
    overlay.querySelectorAll('a[href]').forEach((a) => {
      if (a.getAttribute('href').startsWith('#')) return;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    });
  }

  // Views we could not match to a source file, so Dropbox's own rendering is
  // left in place. Retried when the view's text or the known URLs change.
  const failed = new WeakMap();
  const pending = new WeakSet();

  // Covers Dropbox's rendered view with our rendering of the same file.
  async function attach(container, view, attempt) {
    const host = document.createElement('div');
    host.className = 'mdp-host';
    host.mdpView = view;
    host.mdpKey = location.href;
    const root = host.attachShadow({ mode: 'open' });

    await applyTheme(root);

    // Shown (empty) right away so Dropbox's styling doesn't flash first.
    const overlay = document.createElement('article');
    overlay.className = 'mdp-overlay markdown-body';
    // Keep keyboard events inside the overlay from reaching Dropbox's viewer
    // shortcuts (e.g. arrow keys switching files).
    overlay.addEventListener('keydown', (e) => e.stopPropagation());
    root.append(overlay);
    if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
    container.appendChild(host);

    const md = await findSource(view.innerText);
    if (!host.isConnected) return;
    if (md === null) {
      host.remove();
      failed.set(view, attempt);
      return;
    }
    render(md, overlay);
  }

  // The visible viewer area. The page can also hold a hidden one, e.g. the
  // file list's quick view behind a full-page preview.
  function findContainer() {
    let best = null;
    for (const el of document.querySelectorAll(PREVIEW_CONTENT)) {
      if (!el.offsetWidth || !el.offsetHeight) continue;
      if (!best || el.offsetWidth * el.offsetHeight > best.offsetWidth * best.offsetHeight) best = el;
    }
    return best;
  }

  function scan() {
    const container = findContainer();
    // Dropbox's Markdown view: the viewer holds a Markdown file but not the
    // plain-text view. In plain-text mode we leave Dropbox's source view alone.
    const view =
      container && isMarkdownFile() && !container.querySelector(TEXT_PREVIEW)
        ? Array.from(container.children).find((c) => !c.classList.contains('mdp-host'))
        : null;

    for (const h of document.querySelectorAll('.mdp-host')) {
      if (!view || h.parentElement !== container || h.mdpView !== view || h.mdpKey !== location.href) h.remove();
    }
    if (!view || container.querySelector(':scope > .mdp-host') || pending.has(container)) return;

    const text = view.innerText.trim();
    if (!text) return; // Dropbox hasn't rendered the file yet.
    const attempt = location.href + '|' + origUrls.length + '|' + text.slice(0, 200);
    if (failed.get(view) === attempt) return;

    pending.add(container);
    attach(container, view, attempt).finally(() => pending.delete(container));
  }

  let timer = 0;
  const schedule = () => {
    if (!timer) timer = setTimeout(() => ((timer = 0), scan()), 300);
  };

  const start = () => {
    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    // Follow Dropbox's theme when the user switches it.
    new MutationObserver(() => {
      document.querySelectorAll('.mdp-host').forEach((h) => applyTheme(h.shadowRoot));
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    schedule();
  };
  if (document.body) start();
  else document.addEventListener('DOMContentLoaded', start, { once: true });
})();
