from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_command_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Скасувати", callback_data="command_cancel")],
    ]
)
