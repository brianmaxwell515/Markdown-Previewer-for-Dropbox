# Privacy Policy

English | [繁體中文](PRIVACY.zh-TW.md)

**Markdown Previewer for Dropbox**
Effective date: October 11, 2026

Markdown Previewer for Dropbox ("the extension") is an open-source browser extension that renders Markdown files in the Dropbox website's file viewer. This policy explains what data the extension accesses and what it does with that data.

## Summary

The extension does **not** collect, store, sell, or transmit any personal data. Everything happens locally in your browser.

## What the extension accesses

When you open a Markdown file in the Dropbox web viewer and click **Preview**, the extension:

1. Reads the text of the file that Dropbox is showing on the page.
2. Downloads the same file from `previews.dropbox.com`, the address Dropbox's own viewer uses. The request uses your existing Dropbox session in your browser, so the extension can only read files you are already viewing.
3. Converts the Markdown to formatted text and displays it on the page.

The file content is kept in memory only while the preview is shown, and is discarded when you leave the page or switch files.

## What the extension does not do

- It does not send your files, file names, or any other data to the developer or to any third party.
- It does not store data on your computer. It does not use extension storage, cookies, or local storage.
- It does not use analytics, tracking, or advertising.
- It does not read your Dropbox password or access token, and it does not change, upload, or delete files.
- It does not load code from the internet. All libraries are bundled with the extension.

## Permissions

| Permission | Why it is needed |
| --- | --- |
| Runs on `https://www.dropbox.com/*` | Adds the **Preview** button to the Dropbox file viewer. |
| Access to `https://previews.dropbox.com/*` | Downloads the original Markdown file that you are viewing, so the preview is complete and accurate. |

## Open source

The full source code is available at <https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox>, so you can verify how it works.

## Changes to this policy

If this policy changes, the updated version will be published at the same address with a new effective date.

## Contact

For questions about this policy, please open an issue at <https://github.com/brianmaxwell515/Markdown-Previewer-for-Dropbox/issues>.

---

This extension is not affiliated with, endorsed by, or sponsored by Dropbox, Inc. Dropbox is a trademark of Dropbox, Inc.
