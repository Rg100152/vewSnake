"""vewSnake constants: banner, endpoints, and default configuration."""

import os

APP_NAME = "vewSnake"
VERSION = "1.0.0"
AUTHOR = "Raj Gautam"

BANNER = """
       ______                   _____                  __
      / ____/___ _____  __     / ___/ ____  ____ _____/ /_____
     / / __/ __ `/ __ \\/ /_/\\  \\__ \\ / __ \\/ __ `/ __  / _ \\_  \\
    / /_/ / /_/ / / / / /_/\\ \\ ___/ / / / / /_/ / /_/ /  __/ / /
    \\____/\\__,_/_/ /_/_/    \\//____/_/ /_/\\__,_/\\__,_/\\___/_/ /
           \\ \\_______________________________________________/
            \\_______________________________________________/

                      [ Image Generator CLI ]
                     Developed by: Raj Gautam
"""

# Free, key-less image generation endpoint (Pollinations.ai).
# {prompt} is replaced with the URL-encoded prompt.
DEFAULT_API_TEMPLATE = "https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&nologo=true"

# Custom API override (e.g. your own FastAPI/ngrok server from server/colab_api_server.py).
# Priority: --api CLI flag > VEWSNAKE_API env var > DEFAULT_API_TEMPLATE.
CUSTOM_API_ENV_VAR = "VEWSNAKE_API"

# Custom API servers take a JSON body: {"prompt": "..."} and return image bytes.
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
REQUEST_TIMEOUT = 120  # seconds

USER_AGENT = f"vewSnake/{VERSION} (CLI image generator; +https://github.com/rajgautam)"


def resolve_endpoint(api_flag: str | None, prompt: str, width: int, height: int) -> tuple[str, bool]:
    """Return (url, is_custom) for the given prompt.

    Custom endpoints receive the prompt as a JSON POST body, so the URL
    is returned as-is. The default endpoint embeds the prompt in the URL.
    """
    custom = api_flag or os.environ.get(CUSTOM_API_ENV_VAR)
    if custom:
        return custom.rstrip("/"), True
    from urllib.parse import quote_plus

    return DEFAULT_API_TEMPLATE.format(prompt=quote_plus(prompt), width=width, height=height), False
