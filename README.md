<div align="center">

```
   ______                   _____                  __
  / ____/___ _____  __     / ___/ ____  ____ _____/ /_____
 / / __/ __ `/ __ \/ /_/\  \__ \ / __ \/ __ `/ __  / _ \_  \
/ /_/ / /_/ / / / / /_/\ \ ___/ / / / / /_/ / /_/ /  __/ / /
\____/\__,_/_/ /_/_/    \//____/_/ /_/\__,_/\__,_/\___/_/ /
       \ \_______________________________________________/
        \_______________________________________________/

                  [ Image Generator CLI ]
                 Developed by: Raj Gautam
```

**A lightweight, open-source AI image generator for the terminal.**
No API key. No signup. No local AI models. Runs on 4GB RAM.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![No API Key](https://img.shields.io/badge/API-key--less-success)](https://pollinations.ai)

</div>

---

## ✨ Features

- 🆓 **Free, key-less API** ([Pollinations.ai](https://pollinations.ai)) — zero setup, works out of the box
- 🖥️ **CLI + GUI** — full terminal experience and a dark-themed Tkinter GUI
- 📐 **Custom resolution** — any size from 64×64 up to 2048×2048
- 🚀 **Lightweight** — all rendering happens in the cloud, perfect for old/low-RAM machines
- 🔌 **Custom API server support** — plug in your own GPU backend (Google Colab + FastAPI + ngrok, see `server/`)
- 📊 Live status feedback, latency metrics, and graceful error handling

---

## 📋 Requirements

- **Python 3.10+** (with `tkinter` for the GUI — usually bundled with Python)
- Dependencies: `requests`, `Pillow` (installed automatically)
- An internet connection

---

## ⚡ Direct Install (from GitHub)

**One command — no clone needed:**

```bash
pip install git+https://github.com/Rg100152/vewSnake.git
```

This installs the package globally with the `vewsnake` and `vewsnake-gui` commands.

**Or the classic clone way:**

```bash
git clone https://github.com/Rg100152/vewSnake.git
cd vewSnake
pip install -e .
```

**Or run it without installing at all:**

```bash
git clone https://github.com/Rg100152/vewSnake.git
cd vewSnake
pip install -r requirements.txt
python3 -m vewsnake.cli -p "your prompt here"
```

---

## 🚀 Quick Start

Generate your first image in 10 seconds:

```bash
# Basic generation (saves vewsnake_output.png in the current folder)
vewsnake -p "A cute cartoon snake looking at a computer screen, anime style"

# Custom output file and resolution
vewsnake -p "cyberpunk city at night, neon lights" -o city.png --width 1280 --height 720

# Clean output for scripting (no ASCII banner)
vewsnake -p "minimalist logo of a snake" --no-banner -o logo.png
```

<div align="center">

| Flag | Description | Default |
|---|---|---|
| `-p`, `--prompt` | Text prompt for the image (**required**) | — |
| `-o`, `--output` | Output file path | `vewsnake_output.png` |
| `--width` | Image width in pixels (64–2048) | `1024` |
| `--height` | Image height in pixels (64–2048) | `1024` |
| `--api` | Custom API endpoint URL | free key-less API |
| `--no-banner` | Hide the ASCII banner | off |
| `--version` | Print version | — |

</div>

---

## 🖼️ GUI Usage

```bash
vewsnake-gui
# or: python3 -m vewsnake.gui
```

Type a prompt, hit **GENERATE IMAGE**, preview the result, and save it anywhere as a PNG.

> **Linux note:** if the GUI fails to open with a `tkinter` error, install it with
> `sudo apt install python3-tk` (Debian/Ubuntu).

---

## 🔌 Optional: Your Own GPU API Server (Free via Google Colab)

Don't want to rely on the public API? Host your own SDXL-Turbo backend for free:

1. Open [Google Colab](https://colab.research.google.com) → **Runtime → Change runtime type → T4 GPU**
2. Paste the contents of [`server/colab_api_server.py`](server/colab_api_server.py) into a cell and run it
3. Copy the printed **ngrok URL** and point vewSnake at it:

```bash
vewsnake -p "your prompt" --api https://xxxx.ngrok-free.app/generate
```

Or set it once with an environment variable:

```bash
export VEWSNAKE_API=https://xxxx.ngrok-free.app/generate   # Linux/macOS
set VEWSNAKE_API=https://xxxx.ngrok-free.app/generate      # Windows CMD
```

---

## 📁 Project Structure

```
vewSnake/
├── vewsnake/                # Core source package
│   ├── __init__.py
│   ├── cli.py               # CLI arguments, flags, routing
│   ├── core.py               # Networking + image processing engine
│   ├── constants.py          # Banner, endpoints, config
│   └── gui.py                # Tkinter GUI frontend
├── server/
│   └── colab_api_server.py   # Self-hosted API server (Google Colab)
├── tests/                    # Unit tests
├── pyproject.toml            # Packaging + command entry points
├── requirements.txt
├── LICENSE                   # MIT
└── README.md
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `vewsnake: command not found` | Re-run `pip install -e .`, or use `python3 -m vewsnake.cli` |
| Network timeout | Check your internet connection; retry (free API can be slow) |
| `UnidentifiedImageError` | Your `--api` URL is invalid — verify the ngrok endpoint |
| GUI won't open (Linux) | `sudo apt install python3-tk` |

---

## 📄 License

MIT — see [LICENSE](LICENSE).

Developed by **Raj Gautam** · [github.com/Rg100152](https://github.com/Rg100152)
