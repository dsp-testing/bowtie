#!/usr/bin/env python3
"""
mandelbrot.py - render the Mandelbrot set to a self-contained HTML file.

This script has no third-party dependencies. It computes an escape-time
Mandelbrot fractal, encodes the result as a PNG image (using a small
hand-rolled PNG encoder built on the standard library's ``zlib`` module),
embeds that image as a base64 data URI, and writes a single HTML file that
can be opened directly in a browser.

Usage:
    python mandelbrot.py [-o OUTPUT] [--width W] [--height H]
                         [--max-iter N] [--center-x X] [--center-y Y]
                         [--zoom Z] [--color {classic,fire,ocean,grayscale}]

Examples:
    # Default full-set render
    python mandelbrot.py -o mandelbrot.html

    # Zoom into a seahorse-valley region with more detail
    python mandelbrot.py --center-x -0.743643887037151 \\
                         --center-y 0.13182590420533 \\
                         --zoom 5000 --max-iter 500 -o seahorse.html

"""

from __future__ import annotations

import argparse
import base64
import colorsys
import math
import struct
import zlib
from pathlib import Path

# --------------------------------------------------------------------------
# Mandelbrot computation
# --------------------------------------------------------------------------


def mandelbrot_escape(
    cx: float, cy: float, max_iter: int
) -> tuple[int, float]:
    """Return escape iteration count for ``c = cx + cy*i``.

    Returns the number of iterations before ``c`` escapes the Mandelbrot
    set (or ``max_iter`` if it never does), along with a "smoothed"
    fractional iteration count used for continuous coloring.
    """
    x = 0.0
    y = 0.0
    x2 = 0.0
    y2 = 0.0
    iteration = 0
    while x2 + y2 <= 4.0 and iteration < max_iter:
        y = 2.0 * x * y + cy
        x = x2 - y2 + cx
        x2 = x * x
        y2 = y * y
        iteration += 1

    if iteration >= max_iter:
        return max_iter, float(max_iter)

    # Smooth coloring: fractional escape count avoids visible color bands.
    log_zn = math.log(x2 + y2) / 2.0
    nu = math.log(log_zn / math.log(2)) / math.log(2)
    smooth = iteration + 1 - nu
    return iteration, smooth


def render_mandelbrot(
    width: int,
    height: int,
    max_iter: int,
    center_x: float,
    center_y: float,
    zoom: float,
    color_scheme: str,
) -> bytes:
    """Render the set, returning raw RGB pixel bytes (row-major)."""
    pixels = bytearray(width * height * 3)

    # The view spans 3.5 units wide at zoom == 1, centered on
    # (center_x, center_y).
    scale = 3.5 / zoom
    aspect = height / width
    x_min = center_x - scale / 2
    x_max = center_x + scale / 2
    y_min = center_y - (scale * aspect) / 2
    y_max = center_y + (scale * aspect) / 2

    colorize = _COLOR_SCHEMES[color_scheme]

    for py in range(height):
        cy = (
            y_min + (py / (height - 1)) * (y_max - y_min)
            if height > 1
            else y_min
        )
        row_offset = py * width * 3
        for px in range(width):
            cx = (
                x_min + (px / (width - 1)) * (x_max - x_min)
                if width > 1
                else x_min
            )
            iteration, smooth = mandelbrot_escape(cx, cy, max_iter)
            r, g, b = colorize(iteration, smooth, max_iter)
            idx = row_offset + px * 3
            pixels[idx] = r
            pixels[idx + 1] = g
            pixels[idx + 2] = b

    return bytes(pixels)


# --------------------------------------------------------------------------
# Color schemes
# --------------------------------------------------------------------------


def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def _classic(
    iteration: int, smooth: float, max_iter: int
) -> tuple[int, int, int]:
    if iteration >= max_iter:
        return 0, 0, 0
    hue = (smooth * 0.02) % 1.0
    return _hsv_to_rgb(hue, 0.8, 1.0)


def _fire(
    iteration: int, smooth: float, max_iter: int
) -> tuple[int, int, int]:
    if iteration >= max_iter:
        return 0, 0, 0
    t = (smooth % 32) / 32.0
    r = min(255, int(255 * min(1.0, t * 3)))
    g = min(255, int(255 * max(0.0, min(1.0, t * 3 - 1))))
    b = min(255, int(255 * max(0.0, min(1.0, t * 3 - 2))))
    return r, g, b


def _ocean(
    iteration: int, smooth: float, max_iter: int
) -> tuple[int, int, int]:
    if iteration >= max_iter:
        return 5, 10, 30
    hue = 0.5 + (smooth * 0.015) % 0.3
    return _hsv_to_rgb(hue, 0.7, 1.0)


def _grayscale(
    iteration: int, smooth: float, max_iter: int
) -> tuple[int, int, int]:
    if iteration >= max_iter:
        return 0, 0, 0
    v = int(255 * (smooth % max_iter) / max_iter)
    return v, v, v


_COLOR_SCHEMES = {
    "classic": _classic,
    "fire": _fire,
    "ocean": _ocean,
    "grayscale": _grayscale,
}


# --------------------------------------------------------------------------
# Minimal PNG encoder (stdlib only)
# --------------------------------------------------------------------------


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def encode_png(rgb_pixels: bytes, width: int, height: int) -> bytes:
    """Encode raw RGB pixel bytes as a PNG image, using stdlib zlib only."""
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter type 0 (None) per scanline
        raw.extend(rgb_pixels[y * stride : (y + 1) * stride])

    compressed = zlib.compress(bytes(raw), level=9)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", ihdr)
    png += _png_chunk(b"IDAT", compressed)
    png += _png_chunk(b"IEND", b"")
    return png


# --------------------------------------------------------------------------
# HTML output
# --------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Mandelbrot Set</title>
<style>
  body {{
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #0b0b0f;
    color: #eee;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  h1 {{ font-weight: 300; letter-spacing: 0.05em; margin: 1.2rem 0 0.4rem; }}
  p.meta {{ color: #888; margin: 0 0 1rem; font-size: 0.85rem; }}
  img {{
    max-width: 95vw;
    max-height: 80vh;
    box-shadow: 0 0 40px rgba(0,0,0,0.6);
    image-rendering: pixelated;
  }}
</style>
</head>
<body>
  <h1>Mandelbrot Set</h1>
  <p class="meta">
    {width}x{height}px &middot; max-iter={max_iter} &middot;
    center=({center_x}, {center_y}) &middot; zoom={zoom}x &middot;
    {color_scheme}
  </p>
  <img src="data:image/png;base64,{data}" alt="Mandelbrot set render">
</body>
</html>
"""


def render_html(
    width: int,
    height: int,
    max_iter: int,
    center_x: float,
    center_y: float,
    zoom: float,
    color_scheme: str,
) -> str:
    """Render the Mandelbrot set and return a full HTML document string."""
    pixels = render_mandelbrot(
        width, height, max_iter, center_x, center_y, zoom, color_scheme
    )
    png_bytes = encode_png(pixels, width, height)
    data = base64.b64encode(png_bytes).decode("ascii")
    return HTML_TEMPLATE.format(
        width=width,
        height=height,
        max_iter=max_iter,
        center_x=center_x,
        center_y=center_y,
        zoom=zoom,
        color_scheme=color_scheme,
        data=data,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the renderer."""
    parser = argparse.ArgumentParser(
        description="Render the Mandelbrot set to a self-contained HTML file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("mandelbrot.html"),
        help="Path to the output HTML file (default: mandelbrot.html)",
    )
    parser.add_argument(
        "--width", type=int, default=800, help="Image width in pixels"
    )
    parser.add_argument(
        "--height", type=int, default=600, help="Image height in pixels"
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=200,
        help="Maximum number of escape-time iterations per point",
    )
    parser.add_argument(
        "--center-x",
        type=float,
        default=-0.5,
        help="Real part of the view center",
    )
    parser.add_argument(
        "--center-y",
        type=float,
        default=0.0,
        help="Imaginary part of the view center",
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=1.0,
        help="Zoom factor (larger = more zoomed in)",
    )
    parser.add_argument(
        "--color",
        dest="color_scheme",
        choices=sorted(_COLOR_SCHEMES),
        default="classic",
        help="Color scheme to use (default: classic)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Parse arguments, render the fractal, and write the HTML file."""
    args = parse_args(argv)
    html = render_html(
        width=args.width,
        height=args.height,
        max_iter=args.max_iter,
        center_x=args.center_x,
        center_y=args.center_y,
        zoom=args.zoom,
        color_scheme=args.color_scheme,
    )
    args.output.write_text(html, encoding="utf-8")
    print(f"Wrote {args.output} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
