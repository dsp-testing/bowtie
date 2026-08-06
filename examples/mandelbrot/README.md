# Mandelbrot HTML Renderer

A small, dependency-free Python script that renders the Mandelbrot set and
writes it out as a single, self-contained HTML file you can open directly in
a browser (the image is embedded inline as a base64-encoded PNG).

## Usage

```bash
python mandelbrot.py -o mandelbrot.html
```

Then open `mandelbrot.html` in your browser.

### Options

| Flag | Default | Description |
| --- | --- | --- |
| `-o, --output` | `mandelbrot.html` | Output HTML file path |
| `--width` | `800` | Image width in pixels |
| `--height` | `600` | Image height in pixels |
| `--max-iter` | `200` | Max escape-time iterations per point (higher = more detail, slower) |
| `--center-x` | `-0.5` | Real part of the view center |
| `--center-y` | `0.0` | Imaginary part of the view center |
| `--zoom` | `1.0` | Zoom factor (larger = more zoomed in) |
| `--color` | `classic` | Color scheme: `classic`, `fire`, `ocean`, or `grayscale` |

### Example: zoom into "Seahorse Valley"

```bash
python mandelbrot.py \
  --center-x -0.743643887037151 \
  --center-y 0.13182590420533 \
  --zoom 5000 --max-iter 500 \
  --color fire \
  -o seahorse.html
```

## Notes

* Pure standard library: uses `zlib` to hand-encode a valid PNG and
  `base64` to embed it in the HTML, so no Pillow/numpy/etc. is required.
* Rendering is done in plain Python loops, so very large images or high
  `--max-iter` values will be slow. Adjust the parameters to trade off
  detail versus render time.
