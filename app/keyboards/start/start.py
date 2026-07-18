from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_start_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="👨‍🔧 Адміністрування", callback_data="start_administration")
            ],
            [
                InlineKeyboardButton(text="⚙️ Конфігурація", callback_data="start_configuration"),
                InlineKeyboardButton(text="👨‍💻 Розробник", url="https://t.me/trusres"),

            ],
        ]
    )
