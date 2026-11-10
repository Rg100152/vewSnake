"""Tests for vewsnake.cli and vewsnake.constants."""

from unittest import mock

import pytest

from vewsnake import cli
from vewsnake.constants import resolve_endpoint


class TestResolveEndpoint:
    def test_default_endpoint_embeds_prompt(self):
        url, is_custom = resolve_endpoint(None, "a red car", 512, 512)
        assert is_custom is False
        assert "pollinations.ai" in url
        assert "a+red+car" in url
        assert "width=512" in url
        assert "height=512" in url

    def test_custom_flag_endpoint(self):
        url, is_custom = resolve_endpoint("https://example.com/generate/", "prompt", 64, 64)
        assert is_custom is True
        assert url == "https://example.com/generate"

    def test_env_var_endpoint(self, monkeypatch):
        monkeypatch.setenv("VEWSNAKE_API", "https://env.example.com")
        url, is_custom = resolve_endpoint(None, "prompt", 64, 64)
        assert is_custom is True
        assert url == "https://env.example.com"

    def test_flag_overrides_env_var(self, monkeypatch):
        monkeypatch.setenv("VEWSNAKE_API", "https://env.example.com")
        url, is_custom = resolve_endpoint("https://flag.example.com", "prompt", 64, 64)
        assert is_custom is True
        assert url == "https://flag.example.com"


class TestParser:
    def test_prompt_is_required(self):
        with pytest.raises(SystemExit):
            cli.build_parser().parse_args([])

    def test_defaults(self):
        args = cli.build_parser().parse_args(["-p", "hello"])
        assert args.prompt == "hello"
        assert args.output == "vewsnake_output.png"
        assert args.api is None
        assert args.width == 1024
        assert args.height == 1024
        assert args.no_banner is False

    def test_invalid_size_rejected(self):
        with pytest.raises(SystemExit):
            cli.build_parser().parse_args(["-p", "hi", "--width", "abc"])
        with pytest.raises(SystemExit):
            cli.build_parser().parse_args(["-p", "hi", "--width", "32"])


class TestMain:
    def test_success_exit_code(self, tmp_path):
        fake_png = tmp_path / "out.png"
        with mock.patch("vewsnake.core.requests.get") as get:
            import io

            from PIL import Image

            buf = io.BytesIO()
            Image.new("RGB", (64, 64)).save(buf, format="PNG")
            get.return_value = mock.Mock(status_code=200, content=buf.getvalue())
            code = cli.main(["-p", "test prompt", "-o", str(fake_png), "--no-banner"])
        assert code == 0
        assert fake_png.exists()

    def test_api_error_exit_code(self, capsys):
        with mock.patch("vewsnake.core.requests.get") as get:
            get.return_value = mock.Mock(status_code=500, text="server exploded")
            code = cli.main(["-p", "test prompt", "--no-banner"])
        assert code == 1
