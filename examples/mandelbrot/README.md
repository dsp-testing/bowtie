# Mandelbrot Set Renderer

A single-file, dependency-free HTML/JavaScript Mandelbrot set renderer using
`<canvas>`.

![Mandelbrot set screenshot](./screenshot.png)

## Usage

Just open `index.html` in a browser - no build step or server needed.

## Controls

- **Click** to zoom in, **Shift+Click** to zoom out
- **Drag** to select a zoom region, or **scroll** to zoom under the cursor
- **Reset View** / **Cycle Palette** buttons

Iteration count auto-increases as you zoom in for sharper detail.

## How it works

Each pixel maps to a point `c` in the complex plane. The classic escape-time
algorithm (`z = z^2 + c`, starting from `z = 0`) counts iterations until
`|z| > 2`; points that never escape are in the set (colored black), others
are colored by escape speed. Cardioid/bulb checks skip iterating on points
already known to be in the set, speeding up rendering of the interior.
