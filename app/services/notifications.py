"""Local, explicit desktop notifications initiated by an authorized admin."""

from __future__ import annotations

import ctypes
import os


class NotificationError(RuntimeError):
    """A local desktop notification could not be displayed."""


def show_notification(message: str, title: str = "Control Panel") -> None:
    """Show a Windows desktop message without interpreting the supplied text."""
    if os.name != "nt":
        raise NotificationError("Сповіщення доступні лише на комп’ютері з Windows.")
    if not message.strip():
        raise NotificationError("Текст сповіщення не може бути порожнім.")
    if len(message) > 1_000:
        raise NotificationError("Текст сповіщення не може перевищувати 1000 символів.")
    result = ctypes.windll.user32.MessageBoxW(None, message, title, 0x40)
    if result == 0:
        raise NotificationError("Windows не змогла показати сповіщення.")
