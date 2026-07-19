"""Explicit, on-demand media capture for the local machine.

The bot never records in the background.  Both capture operations are disabled
unless the person running the bot explicitly sets ENABLE_MEDIA_CAPTURE=true.
"""

from __future__ import annotations

import os
import tempfile
import wave
from pathlib import Path


class MediaCaptureError(RuntimeError):
    """A capture request could not be completed safely."""


def _capture_enabled() -> bool:
    return os.getenv("ENABLE_MEDIA_CAPTURE", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _require_enabled() -> None:
    if not _capture_enabled():
        raise MediaCaptureError(
            "Захоплення медіа вимкнене локально. Встановіть ENABLE_MEDIA_CAPTURE=true "
            "у файлі .env і перезапустіть бота."
        )


def capture_screenshot() -> Path:
    """Capture the current primary display to a temporary PNG file."""
    _require_enabled()
    try:
        from PIL import ImageGrab

        image = ImageGrab.grab()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as output:
            path = Path(output.name)
        image.save(path, "PNG")
        return path
    except Exception as exc:  # Platform display permissions vary.
        raise MediaCaptureError(f"Не вдалося зробити знімок екрана: {exc}") from exc


def capture_audio() -> Path:
    """Record a short microphone clip to a temporary WAV file."""
    _require_enabled()
    try:
        seconds = int(os.getenv("AUDIO_CAPTURE_SECONDS", "10"))
    except ValueError as exc:
        raise MediaCaptureError("AUDIO_CAPTURE_SECONDS має бути цілим числом.") from exc
    if not 1 <= seconds <= 60:
        raise MediaCaptureError("AUDIO_CAPTURE_SECONDS має бути від 1 до 60.")

    try:
        import sounddevice as sd

        sample_rate = 44_100
        recording = sd.rec(
            int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16"
        )
        sd.wait()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output:
            path = Path(output.name)
        with wave.open(str(path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(recording.tobytes())
        return path
    except Exception as exc:
        raise MediaCaptureError(f"Не вдалося записати аудіо: {exc}") from exc
