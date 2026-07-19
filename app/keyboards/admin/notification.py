from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


get_notification_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Скасувати", callback_data="notification_cancel")],
    ]
)
