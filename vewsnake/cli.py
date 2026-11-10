"""vewSnake CLI: argument parsing and command routing."""

import argparse
import sys

from .constants import AUTHOR, CUSTOM_API_ENV_VAR, VERSION
from .core import generate_image


def parse_size(value: str) -> int:
    """Parse a positive integer image dimension."""
    try:
        size = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"size must be an integer, got '{value}'") from exc
    if size < 64 or size > 2048:
        raise argparse.ArgumentTypeError("size must be between 64 and 2048 pixels")
    return size


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vewsnake",
        description=(
            "vewSnake: A high-performance, open-source CLI image generator "
            "optimized for resource-constrained systems. Uses a free, key-less "
            "API by default, or your own custom API server."
        ),
        epilog=f"Developed by {AUTHOR}. Powered by open-source Python frameworks.",
    )
    parser.add_argument(
        "-p", "--prompt",
        type=str,
        required=True,
        help="The textual instruction blueprint for the image model to build.",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="vewsnake_output.png",
        help="Output target file path. Defaults to 'vewsnake_output.png'.",
    )
    parser.add_argument(
        "--api",
        type=str,
        default=None,
        help=(
            "Custom API endpoint (e.g. your ngrok/FastAPI server from Google Colab). "
            f"Can also be set via the {CUSTOM_API_ENV_VAR} environment variable."
        ),
    )
    parser.add_argument(
        "--width",
        type=parse_size,
        default=1024,
        help="Output image width in pixels (64-2048). Defaults to 1024.",
    )
    parser.add_argument(
        "--height",
        type=parse_size,
        default=1024,
        help="Output image height in pixels (64-2048). Defaults to 1024.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress the ASCII banner for scripting / piping usage.",
    )
    parser.add_argument("--version", action="version", version=f"vewSnake {VERSION}")
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns exit code."""
    args = build_parser().parse_args(argv)

    try:
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            width=args.width,
            height=args.height,
            api_url=args.api,
            show_banner=not args.no_banner,
        )
        return 0
    except RuntimeError as error:
        print(f"\n[ERROR] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[HALT] Interruption caught. Gracefully shutting down vewSnake runtime.")
        sys.exit(0)
