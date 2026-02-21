<div align="center">

# GIF ➜ ASCII

**Transform any animated GIF into stunning ASCII art — in your terminal, as an HTML page, or as text files.**

<br>

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-10.0+-EE7724?style=for-the-badge)](https://python-pillow.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Win%20|%20macOS%20|%20Linux-888?style=for-the-badge)]()

<br>

```
   ____ ___ _____       _   ____   ____ ___ ___
  / ___|_ _|  ___|     / \ / ___| / ___|_ _|_ _|
 | |  _ | || |_   ___ / _ \\___ \| |    | | | |
 | |_| || ||  _| |___/ ___ \___) | |___ | | | |
  \____|___|_|      /_/   \_\____/ \____|___|___|
```

<br>

<img src="demo.gif" alt="GIF to ASCII Demo" width="600">

</div>

---

## Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage & Options](#-usage--options)
- [Color Modes](#-color-modes)
- [Export Formats](#-export-formats)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## Features

| Feature | Description |
|---|---|
| **Terminal Playback** | Watch your GIF as a looping ASCII animation directly in the console |
| **True Color Support** | Preserve original GIF colors using 24-bit ANSI escape codes |
| **Solid Color Modes** | Apply a uniform color tint — red, green, blue, yellow, cyan, or magenta |
| **HTML Export** | Generate a self-contained animated HTML page you can share anywhere |
| **TXT Export** | Save all frames into a single text file or individual frame files |
| **Adjustable Width** | Render at any character width to fit your terminal or display |
| **FPS Control** | Set custom playback speed for smooth or cinematic animations |
| **Transparency Handling** | Transparent pixels are automatically rendered as empty space |
| **Cross-Platform** | Works on Windows, macOS, and Linux out of the box |

---

## Demo

```
$ python gif2ascii.py nyan.gif -c original -w 120
```

> The script clears the terminal and loops the animation. Press **Ctrl+C** to stop.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JDIDEK/-FIG2TIG-.git
cd -FIG2TIG-
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Only one dependency: **Pillow** (≥ 10.0)

---

## Quick Start

```bash
# Play a GIF as ASCII art in your terminal
python gif2ascii.py your_animation.gif

# With original colors and wider output
python gif2ascii.py your_animation.gif -c original -w 120
```

If you run the script **without arguments**, a colorful interactive guide is displayed automatically.

---

## Usage & Options

```
python gif2ascii.py <input.gif> [options]
```

| Option | Short | Default | Description |
|---|---|---|---|
| `--width` | `-w` | `80` | Output width in characters |
| `--fps` | `-f` | `15` | Playback speed (frames per second) |
| `--threshold` | `-t` | `30` | Darkness threshold — pixels below this luminance become spaces |
| `--color` | `-c` | *none* | Color mode: `original`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta` |
| `--export-txt FILE` | | | Export all frames to a single `.txt` file |
| `--export-dir DIR` | | | Export each frame as a separate `.txt` file in a directory |
| `--export-html FILE` | | | Generate a standalone animated HTML page |
| `--help` | `-h` | | Show help message and exit |

---

## Color Modes

| Mode | Effect |
|---|---|
| *(default)* | Plain white/gray ASCII — no color codes |
| `original` | Each character inherits the RGB color of the corresponding pixel (24-bit true color) |
| `red` | Entire frame tinted red `(255, 50, 50)` |
| `green` | Matrix-style green `(50, 255, 50)` |
| `blue` | Cool blue tint `(50, 150, 255)` |
| `yellow` | Warm yellow `(255, 255, 50)` |
| `cyan` | Bright cyan `(50, 255, 255)` |
| `magenta` | Vivid magenta `(255, 50, 255)` |

---

## Export Formats

### Text — single file

```bash
python gif2ascii.py animation.gif --export-txt output.txt
```

All frames are written sequentially, separated by `--- FRAME N ---` headers.

### Text — directory of frames

```bash
python gif2ascii.py animation.gif --export-dir frames/
```

Creates `frame_001.txt`, `frame_002.txt`, … — one file per frame.

### HTML — animated web page

```bash
python gif2ascii.py animation.gif -c original --export-html animation.html
```

Generates a standalone HTML file with embedded JavaScript that loops the frames at the specified FPS. Open it in any browser — no server required.

---

## Examples

```bash
# 1. Simple terminal playback at default settings
python gif2ascii.py cat.gif

# 2. Matrix-style green at 120 chars wide, 20 fps
python gif2ascii.py cat.gif -c green -w 120 -f 20

# 3. Preserve original colors
python gif2ascii.py nyan.gif -c original -w 100

# 4. Export a colorful HTML page
python gif2ascii.py nyan.gif -c original --export-html nyan.html

# 5. Extract all frames to individual text files
python gif2ascii.py nyan.gif --export-dir nyan_frames

# 6. Increase threshold to remove darker elements
python gif2ascii.py dark_scene.gif -t 80 -w 100
```

---

## Project Structure

```
.
├── gif2ascii.py        # Main script — all logic in one file
├── requirements.txt    # Python dependencies (Pillow)
└── README.md           # You are here
```

---

## How It Works

1. **Frame extraction** — Each frame of the GIF is read using Pillow's `Image.seek()`.
2. **Resize** — The frame is scaled to the target width, with height adjusted by a `0.55` factor to compensate for the taller-than-wide aspect ratio of terminal characters.
3. **RGBA mapping** — Every pixel is converted to RGBA. Transparent or very dark pixels become spaces.
4. **Luminance → character** — Perceived luminance (`0.299R + 0.587G + 0.114B`) maps onto an 11-character ASCII palette: ` .,:;+*?%#@`
5. **Colorization** — In `original` mode, each character is wrapped in a 24-bit ANSI escape code. In solid color modes, the whole frame is wrapped once.
6. **Output** — Frames are either looped in the terminal (with screen clearing), saved to text, or embedded into an HTML page with a `setInterval` animator.

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ and `@#%*+;:,. `

**[⬆ Back to top](#gif--ascii)**

</div>