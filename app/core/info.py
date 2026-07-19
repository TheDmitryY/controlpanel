"""Small, dependency-free helpers for reporting the local machine state."""

from __future__ import annotations

import os
import platform
import shutil
from datetime import datetime
from html import escape


def _format_bytes(value: int | float) -> str:
    units = ("Б", "КіБ", "МіБ", "ГіБ", "ТіБ")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{amount:.1f} ТіБ"


def _memory() -> tuple[int, int] | None:
    """Return total and available RAM on Linux without an extra package."""
    try:
        fields: dict[str, int] = {}
        for line in open("/proc/meminfo", encoding="utf-8"):
            key, value = line.split(":", 1)
            fields[key] = int(value.split()[0]) * 1024
        return fields["MemTotal"], fields["MemAvailable"]
    except (FileNotFoundError, KeyError, ValueError):
        return None


def _uptime() -> str | None:
    try:
        with open("/proc/uptime", encoding="utf-8") as file:
            seconds = int(float(file.read().split()[0]))
    except (FileNotFoundError, ValueError):
        return None
    days, remainder = divmod(seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes = remainder // 60
    return f"{days} д. {hours} год. {minutes} хв."


def system_status_text() -> str:
    """Return a compact, HTML-safe status report for the machine running the bot."""
    disk = shutil.disk_usage("/")
    disk_used = disk.total - disk.free
    lines = ["<b>📊 Статус системи</b>"]

    uptime = _uptime()
    if uptime:
        lines.append(f"⏱ Час роботи: <code>{uptime}</code>")
    memory = _memory()
    if memory:
        total, available = memory
        lines.append(
            f"🧠 RAM: <code>{_format_bytes(total - available)} / {_format_bytes(total)}</code>"
        )
    lines.append(f"💾 Диск /: <code>{_format_bytes(disk_used)} / {_format_bytes(disk.total)}</code>")
    try:
        one_minute_load = os.getloadavg()[0]
        lines.append(f"⚙️ Навантаження (1 хв): <code>{one_minute_load:.2f}</code>")
    except OSError:
        pass
    lines.append(f"🕒 Оновлено: <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>")
    return "\n".join(lines)


def system_info_text() -> str:
    """Return an HTML-safe static information report for the local machine."""
    return "\n".join(
        (
            "<b>📌 Відомості системи</b>",
            f"💻 ОС: <code>{escape(platform.system())} {escape(platform.release())}</code>",
            f"🏗 Архітектура: <code>{escape(platform.machine())}</code>",
            f"🧩 Процесор: <code>{escape(platform.processor() or 'невідомо')}</code>",
            f"🔢 Ядер CPU: <code>{os.cpu_count() or 'невідомо'}</code>",
            f"🐍 Python: <code>{escape(platform.python_version())}</code>",
        )
    )
