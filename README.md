# Sparky — Synthetic Frame Slots

A standalone HTML demo. Keep `index.html` and `sparky-beaver.png` together, then open `index.html` in a browser. The page generates synthetic values locally and does not connect to sensors or hardware.

The selector spans 32 to 1,048,576 synthetic frame slots in steps of 32. The canvas renders no more than 2,048 display bins; at larger selections, each bin averages multiple groups of 32 synthetic slots. Counts above 65,536 frame slots are visualization-only.

The separate Python array prototype remains configured through 65,536 software slots. The separate synthetic robustness benchmark has been tested only through 32,768 channels. The browser display does not extend either limit and is not evidence of additional physical sensors, independent information, benchmark validation, throughput, or hardware support.
