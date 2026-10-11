/* global marked, DOMPurify, hljs, chrome */
(() => {
  'use strict';

  // Dropbox's file viewer (both /preview/... pages and the quick-view panel in
  // the file list) renders text files inside this container.
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
      }
    }).observe({ type: 'resource', buffered: true });
  } catch (_) {
    // Fall back to reading the DOM only.
  }

  const cssPromise = Promise.all(
    ['lib/github-markdown.css', 'lib/hljs-github.min.css', 'lib/hljs-github-dark.min.css', 'preview.css'].map((p) =>
      fetch(chrome.runtime.getURL(p)).then((r) => r.text())
    )
  ).then(([gh, hlLight, hlDark, own]) =>
    [
      gh,
      `@media (prefers-color-scheme: light) { ${hlLight} }`,
      `@media (prefers-color-scheme: dark) { ${hlDark} }`,
      own,
    ].join('\n')
  ).catch(() => '');

  function isMarkdownFile() {
    if (MD_EXT.test(decodeURIComponent(location.pathname))) return true;
    if (origUrls.length && ORIG_MD.test(origUrls[origUrls.length - 1])) return true;
    // Quick-view title bar reads e.g. "00_總表MD • 6.71 KB"
    const qv = document.querySelector(QUICKVIEW_TITLE);
    return !!qv && /(MD|MARKDOWN|MDX)\s*•/.test(qv.textContent);
  }

  function readDomText(viewer) {
    const lines = viewer.querySelectorAll('[data-slate-node="element"]');
    if (!lines.length) return viewer.innerText;
    return Array.from(lines, (li) => li.textContent.replace(/[\uFEFF\u200B]/g, '')).join('\n');
  }

  // Make sure the fetched file is the one currently shown (the last preview URL
  // could belong to a previously opened file).
  function sameFile(fetched, domText) {
    const norm = (s) => s.replace(/\s+/g, '');
    const probe = domText.split('\n').map(norm).filter(Boolean).slice(0, 5);
    if (!probe.length) return true;
    const body = norm(fetched);
    return probe.every((l) => body.includes(l));
  }

  async function getMarkdown(viewer) {
    const domText = readDomText(viewer);
    const candidates = origUrls.filter((u) => ORIG_MD.test(u)).reverse().slice(0, 5);
    for (const url of candidates) {
      try {
        const r = await fetch(url, { credentials: 'include' });
        if (!r.ok) continue;
        const text = await r.text();
        if (sameFile(text, domText)) return text;
      } catch (_) {
        // Try the next candidate, then fall back to the DOM text.
      }
    }
    return domText;
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

  async function attach(container, viewer) {
    const host = document.createElement('div');
    host.className = 'mdp-host';
    host.mdpViewer = viewer;
    host.mdpKey = location.href;
    const root = host.attachShadow({ mode: 'open' });

    const css = await cssPromise;
    try {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(css);
      root.adoptedStyleSheets = [sheet];
    } catch (_) {
      const style = document.createElement('style');
      style.textContent = css;
      root.appendChild(style);
    }

    const button = document.createElement('button');
    button.className = 'mdp-toggle';
    button.type = 'button';
    button.textContent = 'Preview';
    button.setAttribute('aria-pressed', 'false');
    button.title = 'Render this Markdown file';

    const overlay = document.createElement('article');
    overlay.className = 'mdp-overlay markdown-body';
    overlay.hidden = true;

    button.addEventListener('click', async () => {
      const show = overlay.hidden;
      if (show) {
        overlay.innerHTML = '<p class="mdp-status">Loading…</p>';
        overlay.hidden = false;
        button.textContent = 'Source';
        button.setAttribute('aria-pressed', 'true');
        try {
          render(await getMarkdown(host.mdpViewer), overlay);
        } catch (err) {
          overlay.textContent = 'Failed to render Markdown: ' + err;
        }
        overlay.scrollTop = 0;
      } else {
        overlay.hidden = true;
        button.textContent = 'Preview';
        button.setAttribute('aria-pressed', 'false');
      }
    });

    // Keep wheel/keyboard events inside the overlay from reaching Dropbox's
    // viewer shortcuts (e.g. arrow keys switching files).
    overlay.addEventListener('keydown', (e) => e.stopPropagation());

    root.append(button, overlay);
    if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
    container.appendChild(host);
  }

  const pending = new WeakSet();

  function scan() {
    const viewer = document.querySelector(TEXT_PREVIEW);
    const existing = document.querySelectorAll('.mdp-host');
    if (!viewer || !isMarkdownFile()) {
      existing.forEach((h) => h.remove());
      return;
    }
    const container = viewer.closest(PREVIEW_CONTENT) || viewer.parentElement;
    existing.forEach((h) => {
      if (h.parentElement !== container) h.remove();
    });
    const host = container.querySelector(':scope > .mdp-host');
    if (host) {
      // Another file was opened in the same viewer: return to source view.
      if (host.mdpViewer !== viewer || host.mdpKey !== location.href) {
        host.remove();
      } else {
        return;
      }
    }
    if (pending.has(container)) return;
    pending.add(container);
    attach(container, viewer).finally(() => pending.delete(container));
  }

  let timer = 0;
  const schedule = () => {
    if (!timer) timer = setTimeout(() => ((timer = 0), scan()), 300);
  };

  const start = () => {
    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    schedule();
  };
  if (document.body) start();
  else document.addEventListener('DOMContentLoaded', start, { once: true });
})();
