# Mandelbrot Set Renderer

A small, dependency-free Mandelbrot set renderer built with plain JavaScript
and the HTML5 Canvas API.

## Usage

Open `index.html` in any modern web browser (no build step or server
required):

```sh
open examples/mandelbrot/index.html   # macOS
xdg-open examples/mandelbrot/index.html   # Linux
```

## Features

- Smooth (continuous) coloring using the fractional escape-time algorithm.
- Interactive zoom: scroll the mouse wheel, or click to zoom in
  (shift+click to zoom out).
- Drag to pan around the set.
- Iteration budget automatically increases as you zoom in, revealing finer
  detail.
- "Reset View" button restores the default view; "Save PNG" downloads the
  current render as an image.
- Early-out checks for the main cardioid and period-2 bulb speed up
  rendering of large interior regions.
