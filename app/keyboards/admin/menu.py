from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_admin_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="📊 Статус системи", callback_data="admin_status"),
                InlineKeyboardButton(text="📌 Відомості системи", callback_data="admin_info"),
            ],
        ]
    )
