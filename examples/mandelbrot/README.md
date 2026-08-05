# Mandelbrot Set Renderer

A single-file, dependency-free HTML/JavaScript renderer for the Mandelbrot
set, using the `<canvas>` element and the 2D rendering context.

![Mandelbrot set screenshot](./screenshot.png)

## Files

- `index.html` - the entire renderer: markup, styling, and JavaScript logic
  all live in this one file.
- `screenshot.png` - a preview of the default view, shown above.

## Usage

Open `index.html` directly in any modern web browser (no build step or
server required). It also works fine served statically, e.g.:

```sh
python3 -m http.server -d examples/mandelbrot 8000
# then visit http://localhost:8000/
```

### Controls

- **Click** a point to zoom in on it.
- **Shift+Click** a point to zoom out.
- **Drag** to select a rectangular region to zoom into.
- **Scroll** to zoom in/out under the cursor.
- **Reset View** button restores the initial view.
- **Cycle Palette** button switches between color schemes (classic, fire,
  grayscale).

Iteration count automatically increases as you zoom in, to keep detail
sharp at deeper zoom levels.

## How it works

The renderer maps every pixel on the canvas to a point `c = (cx, cy)` in the
complex plane, then runs the classic escape-time algorithm: starting from
`z = 0`, it repeatedly applies `z = z^2 + c` and counts how many iterations
it takes for `|z|` to exceed 2 (escape), up to a maximum iteration count.
Points that never escape are considered part of the Mandelbrot set and are
colored black; points that escape are colored based on how quickly they did,
using one of a few gradient palettes.

Two early-out checks (the main cardioid and period-2 bulb formulas) skip the
iteration loop entirely for points already known to be in the set, which
noticeably speeds up rendering of the interior "blob" regions.

As you zoom in, the maximum iteration count is increased automatically so
that finer detail near the fractal's boundary stays visible instead of
washing out.

## Browser support

Works in any modern browser with `<canvas>` 2D context support (Chrome,
Firefox, Safari, Edge). No external dependencies or build tooling required.
