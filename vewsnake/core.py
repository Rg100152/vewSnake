"""vewSnake core engine: networking, image processing, and console feedback."""

import io
import sys
import time

import requests
from PIL import Image

from .constants import AUTHOR, BANNER, REQUEST_TIMEOUT, USER_AGENT, VERSION, resolve_endpoint


def print_banner() -> None:
    """Print the ASCII banner and engine header."""
    print(BANNER)
    print("=====================================================================")
    print(f"[STATUS] Initializing vewSnake Core Engine v{VERSION}...")
    print(f"[AUTHOR] {AUTHOR}")
    print("=====================================================================")


def generate_image(
    prompt: str,
    output_path: str,
    width: int = 1024,
    height: int = 1024,
    api_url: str | None = None,
    show_banner: bool = True,
) -> str:
    """Generate an image from a prompt and save it to output_path.

    Returns the output path on success. Raises RuntimeError on failure.
    """
    if show_banner:
        print_banner()
    print(f"[TARGET] Output Path Vector : {output_path}")
    print(f"[PROMPT] Payload String     : '{prompt}'")
    print(f"[SIZE]   Resolution         : {width}x{height}")

    url, is_custom = resolve_endpoint(api_url, prompt, width, height)
    print(f"[API]    Endpoint           : {url}")

    start_time = time.time()
    try:
        sys.stdout.write("[PROCESSING] Transmitting data packets to inference engine... ")
        sys.stdout.flush()

        if is_custom:
            response = requests.post(
                url,
                json={"prompt": prompt},
                timeout=REQUEST_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )
        else:
            response = requests.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT})

        if response.status_code != 200:
            sys.stdout.write("FAILED.\n")
            raise RuntimeError(
                f"HTTP Pipeline Exception. Status Code returned: {response.status_code}\n"
                f"Server Response Diagnostics: {response.text[:300]}"
            )

        sys.stdout.write("DONE.\n")
        sys.stdout.write("[COMPILING] Instantiating byte-stream layout into PIL framework... ")
        sys.stdout.flush()

        image = Image.open(io.BytesIO(response.content))
        if image.width != width or image.height != height:
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(output_path)

        sys.stdout.write("SUCCESS.\n")
        elapsed = time.time() - start_time
        print("\n---------------------------------------------------------------------")
        print(f"[TRANSACTION COMPLETED] Image compiled successfully: {output_path}")
        print(f"[METRIC] Total pipeline latency: {elapsed:.2f} seconds.")
        print("---------------------------------------------------------------------")
        return output_path

    except requests.exceptions.Timeout as exc:
        sys.stdout.write("TIMEOUT.\n")
        raise RuntimeError("Network connection timed out. Verify your internet connection.") from exc
    except requests.exceptions.ConnectionError as exc:
        sys.stdout.write("CRASHED.\n")
        raise RuntimeError(f"Connection fault: could not reach the inference endpoint: {exc}") from exc
    except Image.UnidentifiedImageError as exc:
        sys.stdout.write("FAILED.\n")
        raise RuntimeError("Server response was not a valid image. Check the API endpoint URL.") from exc
