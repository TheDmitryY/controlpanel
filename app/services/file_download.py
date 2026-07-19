"""Safe handling of files intentionally sent to the bot by an administrator."""

from __future__ import annotations

import os
import re
from pathlib import Path

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
_UNSAFE_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class FileDownloadError(RuntimeError):
    """A Telegram document cannot be saved safely."""


def downloads_directory() -> Path:
    """Return the conventional Downloads folder, including on Windows."""
    home = Path(os.environ.get("USERPROFILE", Path.home())) if os.name == "nt" else Path.home()
    return home / "Downloads"


def safe_download_path(original_name: str | None, size: int | None) -> Path:
    """Validate a Telegram document and reserve a non-overwriting local path."""
    if size is not None and size > MAX_UPLOAD_BYTES:
        raise FileDownloadError("Розмір файлу перевищує дозволені 50 МіБ.")

    filename = Path(original_name or "telegram_file").name
    filename = _UNSAFE_FILENAME_CHARS.sub("_", filename).strip(". ") or "telegram_file"
    directory = downloads_directory()
    directory.mkdir(parents=True, exist_ok=True)

    candidate = directory / filename
    stem, suffix = candidate.stem, candidate.suffix
    counter = 1
    while candidate.exists():
        candidate = directory / f"{stem} ({counter}){suffix}"
        counter += 1
    return candidate
