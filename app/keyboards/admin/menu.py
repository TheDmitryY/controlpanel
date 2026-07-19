from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_admin_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="📊 Статус системи", callback_data="admin_status"),
                InlineKeyboardButton(text="📌 Відомості системи", callback_data="admin_info"),
            ],
            [
                InlineKeyboardButton(text="📸 Знімок екрана", callback_data="capture_screenshot"),
                InlineKeyboardButton(text="🎙 Записати аудіо", callback_data="capture_audio"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="start_administration"),
            ],
        ]
    )
