from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_download_back_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="start_administration"),
            ],
        ]
    )
