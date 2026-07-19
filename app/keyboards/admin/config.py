from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_configuration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📄 Логи бота", callback_data="config_logs"),
        InlineKeyboardButton(text="🧠 Топ 15 за RAM", callback_data="config_top_memory")],
        [InlineKeyboardButton(text="⬅️ Командний рядок", callback_data="send_command")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="end_configuration")],
    ]
)

get_log_delivery_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💬 Показати в Telegram", callback_data="config_logs_message")],
        [InlineKeyboardButton(text="📎 Надіслати .log файл", callback_data="config_logs_file")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="start_administration")],
    ]
)
