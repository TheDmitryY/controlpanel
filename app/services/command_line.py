import subprocess

class CommandExecuteError(RuntimeError):
    """Custom exception raised for errors when executing a command"""


def enter_command(command: str):
    try:
        subprocess.run(
        [command],
        check=True,
        capture_output=True,
        text=True,
    )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CommandExecuteError(f"{exc}")