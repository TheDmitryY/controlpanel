from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.keyboards.admin.start import get_admin_keyboard
from app.keyboards.admin.menu import get_admin_menu_keyboard
from app.callbacks.data import CallbacksManager
router = Router()
text = """🪛 Меню адміністрування\n \nОберіть дію: \n"""

callback_manager = CallbacksManager.get()

@router.callback_query(F.data.in_(callback_manager))
async def callbacks_start(callback: CallbackQuery):
    callback_data = callback.data
    match callback_data:
        case "start_administration":
            await callback.message.edit_text(
                text=text,
                reply_markup=get_admin_keyboard,
                parse_mode="HTML"
                )
            await callback.answer()
        case "admin_menu":
            await callback.message.edit_text(
                text="🪛 Меню керування\n \nОберіть дію: \n",
                reply_markup=get_admin_menu_keyboard,
                parse_mode="HTML"
            )
            await callback.answer()