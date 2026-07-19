import os
import json
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers.start import router as start_router
from app.callbacks.start import router as start_callbacks
from app.middlewars.admin import AdminAccessMiddleware
from app.core.diagnostics import BOT_LOG_PATH

BASE_DIR = Path(__file__).resolve().parent
BOT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(BOT_LOG_PATH, maxBytes=512 * 1024, backupCount=2, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# Locate and load the .env file relative to the script's directory
ENV_PATH = BASE_DIR / '.env'

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    logger.info(f"Loaded environment variables from {ENV_PATH}")
else:
    logger.warning(f"No .env file found at {ENV_PATH}, using system environment variables.")

# Retrieve and validate environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment or .env file.")

raw_admins = os.getenv("ADMIN_TELEGRAM_ID", "")
ADMIN_IDS = {int(admin_id) for admin_id in raw_admins.split(",") if admin_id.strip().isdigit()}

OWNER_TG_ID_RAW = os.getenv('OWNER_TG_ID')
if not OWNER_TG_ID_RAW:
    raise ValueError("OWNER_TG_ID is not set in the environment or .env file.")
try:
    OWNER_ID = int(OWNER_TG_ID_RAW.strip())
except ValueError as e:
    raise ValueError(f"Failed to parse OWNER_TG_ID as an integer: {e}")

# The declared owner is always permitted to use this locally hosted bot.
ADMIN_IDS.add(OWNER_ID)

# Initialize Bot
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def on_startup() -> None:
    logger.info("Bot startup tasks...")

async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.middleware(AdminAccessMiddleware(admin_ids=ADMIN_IDS))
    dp.callback_query.middleware(AdminAccessMiddleware(admin_ids=ADMIN_IDS))
    dp.include_routers(
        start_router,
        start_callbacks
    )
    try:
        await on_startup()
        logger.info("Starting bot polling...")

        await dp.start_polling(bot, skip_updates=True)
    finally:
        logger.info("Shutdown initiated. Cleaning up resources...")
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{current_time_end} Bot stopped by host")
