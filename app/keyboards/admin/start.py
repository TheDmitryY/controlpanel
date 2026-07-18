from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="👨‍💻 Керування", callback_data="admin_menu")
            ],
        ]
    )
