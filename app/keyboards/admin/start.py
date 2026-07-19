from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="👨‍💻 Керування", callback_data="admin_menu"),
                InlineKeyboardButton(text="🕹 Гібернація", callback_data="power_menu")
            ],
            [
                InlineKeyboardButton(text="📦 Завантаження", callback_data="admin_download")
            ],
            [
                InlineKeyboardButton(text="🔔 Сповіщення", callback_data="send_notification"),
            ],
        ]
    )
