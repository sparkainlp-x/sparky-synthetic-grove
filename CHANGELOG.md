# Changelog

All values in this project are SYNTHETIC.

## 0.1.0 (2026-10-18)

First public release candidate.

### Added
- AGPL-3.0-only LICENSE, CITATION.cff and .zenodo.json (community `spark-ai-nlp`).
- Standard-library page checks (`tests/test_page.py`): alt text, labelled controls, reduced motion, no external requests, image size, no decorative symbols or banned claims, and an inline-script syntax check with Node when available.
- CI on Python 3.10-3.13 and a GitHub Pages workflow that publishes only `index.html` and the mascot image.
- Skip link, figure caption for the mascot, status role for the animation state, footer with copyright, licence and source link, and a strict Content-Security-Policy.

### Changed
- Mascot image: 4.6 MB PNG (1920 x 1920) replaced by a 100 KB WebP (768 x 768, transparency kept).
- Colours: Sparky brand palette, gold #c9a84c on navy with cyan.
- Decorative symbols removed (brand mark, eyebrow sparkle, detail icons); the pause and resume icon is drawn in CSS.
- README rewritten with quickstart, evidence labels, limitations, accessibility notes and citation.

### Removed
- `wrangler.jsonc` (a Cloudflare preview configuration that would have published the whole directory).

## Before 0.1.0

- Initial import of the standalone page and a copy review of the guide text (pull request #1).
