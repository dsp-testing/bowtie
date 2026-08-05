# Mandelbrot Set Renderer

A single-file, dependency-free HTML/JavaScript renderer for the Mandelbrot
set, using the `<canvas>` element and the 2D rendering context.

## Usage

Open `index.html` directly in any modern web browser (no build step or
server required).

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
