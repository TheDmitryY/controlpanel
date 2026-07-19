## Control Panel

Telegram bot with an inline admin menu for on-demand local system actions.

### Setup

Create `.env` beside `main.py`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
OWNER_TG_ID=your_telegram_id
# Optional additional IDs, comma-separated
ADMIN_TELEGRAM_ID=123456789

# Explicitly authorize capture on the machine running the bot.
ENABLE_MEDIA_CAPTURE=true
# Optional; integer from 1 through 60 (default: 10)
AUDIO_CAPTURE_SECONDS=10
```

Install the project dependencies, then run `python main.py`. The owner and
listed admin IDs can open the inline menu. Each button immediately updates the
menu text with its status; screenshots and microphone clips are captured only
when their button is pressed. Media capture is disabled by default.

The `📦 Завантаження` action accepts a document from an authorized admin and
saves it to the host computer's `Downloads` folder (on Windows,
`%USERPROFILE%\\Downloads`). Files are not opened or executed; uploads are
limited to 50 MiB and a duplicate filename receives a numeric suffix.

The `⚙️ Конфігурація` menu can show the last 50 log records in Telegram or send
the current log file, and report the 15 processes using the most RAM. Logs rotate automatically: the active file is capped at
512 KiB, with two backups, to keep disk use bounded.

The `🔔 Сповіщення` action lets an authorized admin send up to 1,000 characters
to a local Windows desktop notification. The text is displayed as text only;
it is never interpreted as a command.

On Linux, microphone capture may require a system PortAudio package and desktop
screen capture may require a graphical session with screen-recording permission.
