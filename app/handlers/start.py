from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import os, json
from app.keyboards.start.start import get_start_keyboard

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_ID


ADMIN_ID = json.loads(os.getenv('ADMIN_TELEGRAM_ID', "[]"))

router = Router()

@router.message(Command("start"))
async def welcome(message: Message):
    full_name = message.from_user.full_name
    text = f"""
    \n <b> 👋 Ласкаво просимо {full_name}! </b>
      \n \n <b>ControlPanel - віддаленний телеграм бот для адміністрування та керування персональним комп'ютером</b>
      \n \n <i> ❌ Дії можуть бути небезпечними!</i>
      \n \n <i> 🔽 Натискай кнопки і вперед!</i>
      """
    start_responce = await message.reply(text, reply_markup=get_start_keyboard, parse_mode="HTML") 


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("🔧 Щоб розпочати, натисніть кнопку нижче! Також ви можете звернутися до технічної підтримки!", reply_markup=help_kb, parse_mode="HTML")
