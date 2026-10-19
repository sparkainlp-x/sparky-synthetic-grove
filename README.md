# Sparky Synthetic Grove

A standalone HTML page in which Sparky the beaver guides you through a grid of **synthetic** frame slots. Pick a count from 32 to 1,048,576 in steps of 32; the page groups the slots 32 at a time and draws at most 2,048 display bins on a canvas. Every value is generated in your browser by a fixed wave formula. Nothing is measured, and the page connects to no sensor, device or network.

Live page: [sparkainlp-x.github.io/sparky-synthetic-grove](https://sparkainlp-x.github.io/sparky-synthetic-grove/) (enabled at launch).

## Quickstart

No build step and no dependencies. Keep `index.html` and `sparky-beaver.webp` together and open `index.html` in a browser:

```bash
git clone https://github.com/sparkainlp-x/sparky-synthetic-grove
cd sparky-synthetic-grove
python3 -m http.server 8000      # then open http://localhost:8000/ (or open index.html directly)
python3 -W error -m unittest discover -s tests -v   # static page checks
```

## What it shows

- A slider and four presets (4,096, 32,768, 65,536 and 1,048,576 slots).
- Three readouts: selected slots, groups of 32, and the browser visualization ceiling.
- A canvas map of grouped synthetic values. At larger selections each display bin averages several groups of 32 slots, and the caption says how many.
- A pause control. With reduced motion requested by the operating system, the map starts paused.

## Evidence labels

- **SYNTHETIC:** every value on the page, generated in the browser.
- **UNRUN:** any use with real sensor data; the page has no data input.
- No number on the page is REPORTED (measured on named real data) or a performance TARGET.

## Limitations

- Counts above 65,536 frame slots are visualization-only. The separate Python array prototype ([oes32-membrane-array](https://github.com/sparkainlp-x/oes32-membrane-array)) remains configured through 65,536 software slots, and the separate synthetic robustness benchmark has been tested only through 32,768 channels. The browser display does not extend either limit.
- The display is not evidence of additional physical sensors, independent information, benchmark results, throughput or hardware support.
- The wave formula is decorative and deterministic; the map does not model any physical process.
- The canvas is described to assistive technology by a text summary that updates with the selection, not cell by cell.

## Accessibility

Keyboard-operable slider, presets and pause button with visible focus; a skip link; described mascot image and canvas; a live status for the animation state; `prefers-reduced-motion` honoured in CSS and JavaScript; secondary text colours chosen for at least 4.5:1 contrast against the page background and the main panel colour. The checks in `tests/test_page.py` run in CI.

## Privacy and security

No cookies, analytics, fonts or other external requests. A Content-Security-Policy allows only the page's own image plus its inline style and script.

## How to cite

See [CITATION.cff](CITATION.cff). A Zenodo DOI will be listed here after the first release: `10.5281/zenodo.XXXXXXX` (placeholder).

> Brisson, J.-F. (2026). *Sparky Synthetic Grove: a standalone browser visualization of synthetic frame slots* (Version 0.1.0) [Computer software]. Spark AI NLP, Fredericton, New Brunswick, Canada. https://github.com/sparkainlp-x/sparky-synthetic-grove

## License

Copyright (c) 2026 Jean-François Brisson, Spark AI NLP.

Released under the GNU Affero General Public License v3.0 only (AGPL-3.0-only); see [LICENSE](LICENSE). The Sparky name and mascot artwork identify this project.
