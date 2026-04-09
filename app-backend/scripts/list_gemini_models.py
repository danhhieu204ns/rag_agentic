from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _load_env_file(env_path: Path) -> None:
    """Load KEY=VALUE pairs from a .env file into process environment."""

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _list_models(api_key: str, api_version: str) -> list[dict]:
    query = urlencode({"key": api_key})
    url = f"https://generativelanguage.googleapis.com/{api_version}/models?{query}"
    request = Request(url, method="GET")

    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} when listing models on {api_version}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error when listing models on {api_version}: {exc}") from exc

    return payload.get("models", [])


def _supports_embed(model: dict) -> bool:
    methods = model.get("supportedGenerationMethods") or []
    methods = [str(item) for item in methods]
    return "embedContent" in methods


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List available Gemini models and show embedding support.",
    )
    parser.add_argument("--api-key", default=None, help="Gemini API key.")
    parser.add_argument(
        "--api-versions",
        default="v1beta,v1",
        help="Comma-separated API versions to try, default: v1beta,v1",
    )
    parser.add_argument(
        "--only-embedding",
        action="store_true",
        help="Only print models that support embedContent.",
    )
    args = parser.parse_args()

    root_env = Path(__file__).resolve().parents[2] / ".env"
    backend_env = Path(__file__).resolve().parents[1] / ".env"
    _load_env_file(root_env)
    _load_env_file(backend_env)

    api_key = args.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY, or pass --api-key.", file=sys.stderr)
        return 1

    versions = [item.strip() for item in args.api_versions.split(",") if item.strip()]
    if not versions:
        print("No API version provided.", file=sys.stderr)
        return 1

    had_success = False
    for version in versions:
        print(f"\n=== {version} ===")
        try:
            models = _list_models(api_key=api_key, api_version=version)
        except RuntimeError as exc:
            print(f"Failed: {exc}")
            continue

        had_success = True

        if not models:
            print("No models returned.")
            continue

        filtered = [m for m in models if _supports_embed(m)] if args.only_embedding else models
        if not filtered:
            print("No matching models.")
            continue

        for model in filtered:
            name = model.get("name", "<unknown>")
            methods = ",".join(model.get("supportedGenerationMethods") or [])
            print(f"- {name} | embedContent={_supports_embed(model)} | methods={methods}")

    if not had_success:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
