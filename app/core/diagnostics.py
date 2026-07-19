"""Bounded local diagnostics used by the configuration menu."""

from __future__ import annotations

import csv
import os
import subprocess
from html import escape
from io import StringIO
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
BOT_LOG_PATH = PROJECT_DIR / "logs" / "bot.log"


def largest_memory_processes_text(limit: int = 15) -> str:
    """Return the local processes using the most resident memory."""
    if os.name == "nt":
        return _windows_largest_memory_processes(limit)
    return _linux_largest_memory_processes(limit)


def log_tail_text(max_lines: int = 50, max_characters: int = 3_500) -> str:
    """Return a bounded, HTML-safe tail of the bot log for a Telegram message."""
    if not BOT_LOG_PATH.exists():
        return "ℹ️ Файл журналу ще не створено."
    try:
        lines = BOT_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return f"⚠️ Не вдалося прочитати журнал: <code>{escape(str(exc))}</code>"
    content = "\n".join(lines[-max_lines:])[-max_characters:]
    if not content:
        return "ℹ️ Журнал порожній."
    return "<b>📄 Останні записи журналу</b>\n<pre>" + escape(content) + "</pre>"


def _windows_largest_memory_processes(limit: int) -> str:
    command = (
        "Get-Process | Sort-Object WorkingSet64 -Descending | "
        f"Select-Object -First {limit} ProcessName,Id,WorkingSet64 | ConvertTo-Csv -NoTypeInformation"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        rows = list(csv.DictReader(StringIO(result.stdout)))
        if not rows:
            raise ValueError("список процесів порожній")
        lines = ["<b>🧠 Топ 15 процесів за RAM</b>"]
        for index, row in enumerate(rows, 1):
            memory_mib = int(row["WorkingSet64"]) / 1024 / 1024
            lines.append(
                f"{index}. <code>{escape(row['ProcessName'])}</code> "
                f"(PID {escape(row['Id'])}) — <code>{memory_mib:.1f} МіБ</code>"
            )
        return "\n".join(lines)
    except (OSError, subprocess.SubprocessError, StopIteration, KeyError, ValueError) as exc:
        return f"⚠️ Не вдалося отримати дані про процеси: <code>{escape(str(exc))}</code>"


def _linux_largest_memory_processes(limit: int) -> str:
    processes: list[tuple[int, str, int]] = []
    try:
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                status = (entry / "status").read_text(encoding="utf-8")
                rss_line = next(line for line in status.splitlines() if line.startswith("VmRSS:"))
                memory_kib = int(rss_line.split()[1])
                name = (entry / "comm").read_text(encoding="utf-8").strip()
                processes.append((memory_kib, name, int(entry.name)))
            except (FileNotFoundError, PermissionError, StopIteration, ValueError):
                continue
    except FileNotFoundError:
        return "⚠️ Дані про процеси недоступні на цій системі."
    if not processes:
        return "⚠️ Не знайдено доступних даних про процеси."
    lines = ["<b>🧠 Топ 15 процесів за RAM</b>"]
    for index, (memory_kib, name, pid) in enumerate(
        sorted(processes, reverse=True)[:limit], 1
    ):
        lines.append(
            f"{index}. <code>{escape(name)}</code> (PID {pid}) — "
            f"<code>{memory_kib / 1024:.1f} МіБ</code>"
        )
    return "\n".join(lines)
