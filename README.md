# vewSnake

A lightweight, open-source CLI image generator optimized for low-resource
systems (works great on 4GB RAM). **No API key, no signup, no local AI
models.**

```
       ______                   _____                  __
      / ____/___ _____  __     / ___/ ____  ____ _____/ /_____
     / / __/ __ `/ __ \\/ /_/\\  \\__ \\ / __ \\/ __ `/ __  / _ \\_  \\
    / /_/ / /_/ / / / / /_/\\ \\ ___/ / / / / /_/ / /_/ /  __/ / /
    \\____/\\__,_/_/ /_/_/    \\//____/_/ /_/\\__,_/\\__,_/\\___/_/ /
           \\ \\_______________________________________________/
            \\_______________________________________________/

                      [ Image Generator CLI ]
                     Developed by: Raj Gautam
```

## Features

- Free, key-less image generation API (Pollinations.ai) by default
- Optional custom API server support (Google Colab + FastAPI + ngrok, see `server/`)
- CLI and Tkinter GUI frontends
- Custom resolution output (`--width` / `--height`)
- ASCII banner, terminal status feedback, and latency metrics
- Runs comfortably on old hardware — all rendering happens in the cloud

## Installation

```bash
cd vewSnake
pip install requests pillow   # dependencies
pip install -e .              # installs the global `vewsnake` command
```

## Usage (CLI)

```bash
# Basic generation (saves vewsnake_output.png)
vewsnake -p "A cute cartoon snake looking at a computer screen, anime style"

# Custom output file and resolution
vewsnake -p "cyberpunk city at night, neon lights" -o city.png --width 1280 --height 720

# Use your own Colab-hosted API server
vewsnake -p "a red apple on a table" --api https://xxxx.ngrok-free.app/generate

# Scripting mode (no banner)
vewsnake -p "minimalist logo of a snake" --no-banner -o logo.png
```

Or without installing:

```bash
python3 -m vewsnake.cli -p "your prompt here"
```

## Usage (GUI)

```bash
vewsnake-gui
# or: python3 -m vewsnake.gui
```

## Custom API Server (optional, free GPU via Google Colab)

1. Open [Google Colab](https://colab.research.google.com), set runtime to **T4 GPU**
2. Copy the contents of `server/colab_api_server.py` into a cell and run it
3. Copy the printed ngrok URL and use it locally:

```bash
vewsnake -p "your prompt" --api https://xxxx.ngrok-free.app/generate
```

You can also export `VEWSNAKE_API=https://...` instead of passing `--api` each time.

## Project Structure

```
vewSnake/
├── vewsnake/          # Core source package
│   ├── __init__.py
│   ├── cli.py         # CLI arguments, flags, routing
│   ├── core.py        # Networking + image processing engine
│   ├── constants.py   # Banner, endpoints, config
│   └── gui.py         # Tkinter GUI frontend
├── server/
│   └── colab_api_server.py   # Self-hosted API (Google Colab)
├── tests/              # Unit tests
├── pyproject.toml      # Packaging + global command entry points
├── requirements.txt
├── LICENSE             # MIT
└── README.md
```

## Running Tests

```bash
pip install pytest
pytest
```

## License

MIT — see [LICENSE](LICENSE). Developed by **Raj Gautam**.
