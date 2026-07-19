"""Explicit Windows power-session actions requested through the admin bot."""

from __future__ import annotations

import ctypes
import os
import subprocess


class PowerControlError(RuntimeError):
    """A requested local power action cannot be performed."""


def _require_windows() -> None:
    if os.name != "nt":
        raise PowerControlError("Ця дія доступна лише на комп’ютері з Windows.")


def schedule_shutdown(seconds: int) -> None:
    """Schedule a Windows shutdown using ``shutdown /s /t``."""
    _require_windows()
    if not 0 <= seconds <= 86_400:
        raise PowerControlError("Таймер вимкнення має бути від 0 до 86400 секунд.")
    try:
        subprocess.run(
            ["shutdown", "/s", "/t", str(seconds)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PowerControlError(f"Не вдалося запланувати вимкнення: {exc}") from exc


def lock_workstation() -> None:
    """Lock the interactive Windows workstation (the same outcome as Win+L)."""
    _require_windows()
    if not ctypes.windll.user32.LockWorkStation():
        raise PowerControlError("Windows не дозволила заблокувати цей сеанс.")


def abort_shutdown() -> None:
    """Cancel a pending Windows shutdown timer."""
    _require_windows()
    try:
        subprocess.run(["shutdown", "/a"], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PowerControlError(f"Не вдалося скасувати вимкнення: {exc}") from exc
