from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_power_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⏻ Вимкнути ПК зараз", callback_data="power_shutdown_confirm")],
        [
            InlineKeyboardButton(text="⏱ Через 5 хв", callback_data="power_shutdown_300"),
            InlineKeyboardButton(text="⏱ Через 15 хв", callback_data="power_shutdown_900"),
        ],
        [InlineKeyboardButton(text="⏱ Через 30 хв", callback_data="power_shutdown_1800")],
        [InlineKeyboardButton(text="🔒 Заблокувати комп’ютер", callback_data="power_lock")],
        [InlineKeyboardButton(text="🚫 Скасувати вимкнення", callback_data="power_abort")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu")],
    ]
)

get_shutdown_confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚠️ Так, вимкнути зараз", callback_data="power_shutdown_0")],
        [InlineKeyboardButton(text="⬅️ Скасувати", callback_data="power_menu")],
    ]
)
