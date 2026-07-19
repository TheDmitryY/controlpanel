from aiogram import Bot, Router, F
import asyncio
from pathlib import Path
from collections.abc import Callable
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message
from app.keyboards.admin.start import get_admin_keyboard
from app.keyboards.admin.menu import get_admin_menu_keyboard
from app.callbacks.data import CallbacksManager
from app.core.info import system_info_text, system_status_text
from app.services.media_capture import MediaCaptureError, capture_audio, capture_screenshot
from app.services.file_download import FileDownloadError, safe_download_path
from app.keyboards.admin.download import get_download_back_keyboard
from app.keyboards.admin.power import get_power_keyboard, get_shutdown_confirmation_keyboard
from app.keyboards.start.start import  get_start_keyboard
from app.services.power_control import (
    PowerControlError,
    abort_shutdown,
    lock_workstation,
    schedule_shutdown,
)
from app.core.diagnostics import BOT_LOG_PATH, largest_memory_processes_text, log_tail_text
from app.keyboards.admin.config import get_configuration_keyboard, get_log_delivery_keyboard
from app.keyboards.admin.notification import get_notification_cancel_keyboard
from app.keyboards.admin.command import get_command_cancel_keyboard
from app.services.notifications import NotificationError, show_notification
from app.services.command_line import enter_command, CommandExecuteError

router = Router()

callback_manager = CallbacksManager.get()


class UploadFile(StatesGroup):
    waiting_for_document = State()

class Command(StatesGroup):
    waiting_for_command = State()

class Notification(StatesGroup):
    waiting_for_text = State()

@router.callback_query(F.data.in_(callback_manager))
async def callbacks_start(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data
    match callback_data:
        case "start_administration":
            text = """🪛 Меню адміністрування\n \nОберіть дію: \n"""
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

        case "end_configuration":
            full_name = callback.from_user.full_name
            text = f"""
                \n <b> 👋 Ласкаво просимо {full_name}! </b>
                  \n \n <b>ControlPanel - віддаленний телеграм бот для адміністрування та керування персональним комп'ютером</b>
                  \n \n <i> ❌ Дії можуть бути небезпечними!</i>
                  \n \n <i> 🔽 Натискай кнопки і вперед!</i>
                  """
            await callback.message.edit_text(text, reply_markup=get_start_keyboard, parse_mode="HTML")
            await callback.answer()

        case "start_configuration":
            await callback.message.edit_text(
                "⚙️ <b>Конфігурація</b>\n\nОберіть діагностичну дію.",
                reply_markup=get_configuration_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()
        case "capture_screenshot":
            await _send_capture(callback, "📸 Створюю знімок екрана…", capture_screenshot, "photo")
        case "capture_audio":
            await _send_capture(callback, "🎙 Записую аудіо…", capture_audio, "audio")
        case "admin_status":
            await callback.message.edit_text(
                system_status_text(), reply_markup=get_admin_menu_keyboard, parse_mode="HTML"
            )
            await callback.answer("Статус оновлено")
        case "admin_info":
            await callback.message.edit_text(
                system_info_text(), reply_markup=get_admin_menu_keyboard, parse_mode="HTML"
            )
            await callback.answer()
        case "admin_download":
            await state.set_state(UploadFile.waiting_for_document)
            await callback.message.edit_text(
                "📦 <b>Завантаження файлу</b>\n\nНадішліть файл як документ. "
                "Його буде збережено в папці <code>Downloads</code> на цьому комп’ютері.\n"
                "Максимальний розмір: 50 МіБ.",
                reply_markup=get_download_back_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()

        case "send_command":
            await state.set_state(Command.waiting_for_command)
            await callback.message.edit_text(
                text="🔔 <b>Виконання команди</b>\n\nНадішліть команду, яку потрібно виконати на комп’ютері.\n",
                parse_mode="HTML",
                reply_markup=get_command_cancel_keyboard
            )
            await callback.answer()

        case "command_cancel":
            await state.clear()
            await callback.message.edit_text(text="Скасовано", reply_markup=get_admin_keyboard, parse_mode="HTML")
            await callback.answer("Виконання скасовано")

        case "send_notification":
            await state.set_state(Notification.waiting_for_text)
            await callback.message.edit_text(
                "🔔 <b>Нове сповіщення</b>\n\nНадішліть текст, який потрібно показати на комп’ютері.\n"
                "Максимум: 1000 символів.",
                reply_markup=get_notification_cancel_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()
        case "notification_cancel":
            await state.clear()
            await callback.message.edit_text(text="Скасовано", reply_markup=get_admin_keyboard, parse_mode="HTML")
            # await callback.answer("Скасовано")

        case "power_menu":
            await callback.message.edit_text(
                "🕹 <b>Керування живленням</b>\n\nОберіть дію для цього комп’ютера.",
                reply_markup=get_power_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()
        case "power_shutdown_confirm":
            await callback.message.edit_text(
                "⚠️ <b>Вимкнути комп’ютер зараз?</b>\n\nНезбережені дані можуть бути втрачені.",
                reply_markup=get_shutdown_confirmation_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()
        case "power_shutdown_0" | "power_shutdown_300" | "power_shutdown_900" | "power_shutdown_1800":
            seconds = int(callback_data.removeprefix("power_shutdown_"))
            await _perform_power_action(callback, schedule_shutdown, seconds)
        case "power_lock":
            await _perform_power_action(callback, lock_workstation)
        case "power_abort":
            await _perform_power_action(callback, abort_shutdown)
        case "config_logs":
            await callback.message.edit_text(
                "📄 <b>Журнал бота</b>\n\nОберіть спосіб отримання.",
                reply_markup=get_log_delivery_keyboard,
                parse_mode="HTML",
            )
            await callback.answer()
        case "config_logs_message":
            await callback.message.edit_text(
                log_tail_text(), reply_markup=get_log_delivery_keyboard, parse_mode="HTML"
            )
            await callback.answer()
        case "config_logs_file":
            await callback.answer()
            if BOT_LOG_PATH.exists():
                await callback.message.answer_document(
                    FSInputFile(BOT_LOG_PATH), caption="📄 Поточний журнал бота"
                )
                await callback.message.edit_text(
                    "✅ Поточний журнал надіслано.", reply_markup=get_configuration_keyboard
                )
            else:
                await callback.message.edit_text(
                    "ℹ️ Файл журналу ще не створено.", reply_markup=get_configuration_keyboard
                )
        case "config_top_memory":
            await callback.message.edit_text(
                largest_memory_processes_text(), reply_markup=get_configuration_keyboard, parse_mode="HTML"
            )
            await callback.answer()


@router.message(StateFilter(UploadFile.waiting_for_document), F.document)
async def receive_document(message: Message, state: FSMContext, bot: Bot) -> None:
    """Download the explicitly supplied Telegram document without executing it."""
    document = message.document
    if document is None:
        return
    try:
        destination = safe_download_path(document.file_name, document.file_size)
        await bot.download(document, destination=destination)
        await state.clear()
        await message.answer(f"✅ Файл збережено: <code>{destination.name}</code>")
    except FileDownloadError as exc:
        await message.answer(f"⚠️ {exc}")
    except Exception:
        await message.answer("⚠️ Не вдалося завантажити файл. Спробуйте ще раз.")


@router.message(StateFilter(UploadFile.waiting_for_document))
async def require_document(message: Message) -> None:
    await message.answer("⚠️ Надішліть файл саме як документ.")


@router.message(StateFilter(Notification.waiting_for_text), F.text)
async def send_notification_text(message: Message, state: FSMContext) -> None:
    try:
        await asyncio.to_thread(show_notification, message.text)
        await message.answer("✅ Сповіщення показано на комп’ютері.")
        await state.clear()
    except NotificationError as exc:
        await message.answer(f"⚠️ {exc}")


@router.message(StateFilter(Notification.waiting_for_text))
async def require_notification_text(message: Message) -> None:
    await message.answer("⚠️ Надішліть текстове повідомлення для сповіщення.")

@router.message(StateFilter(Command.waiting_for_command), F.text)
async def send_command_text(message: Message, state: FSMContext) -> None:
    try:
        await asyncio.to_thread(enter_command, message.text)
        await message.answer("✅ Команда виконана на комп’ютері.")
        await state.clear()
    except CommandExecuteError as exc:
        await message.answer(f"⚠️ {exc}")

@router.message(StateFilter(Command.waiting_for_command))
async def send_command(message: Message) -> None:
    await message.answer("⚠️ Надішліть команду для виконання.\n\n❌ Дії можуть бути небезпечними!\n")

async def _perform_power_action(
    callback: CallbackQuery, action: Callable[..., None], *args: object
) -> None:
    """Run an explicit Windows session action and update the inline message."""
    await callback.answer()
    try:
        await asyncio.to_thread(action, *args)
        if action is schedule_shutdown:
            seconds = int(args[0])
            status = "✅ Вимкнення заплановано зараз." if seconds == 0 else (
                f"✅ Вимкнення заплановано через {seconds // 60} хв."
            )
        elif action is lock_workstation:
            status = "✅ Команду блокування надіслано."
        else:
            status = "✅ Заплановане вимкнення скасовано."
        await callback.message.edit_text(status, reply_markup=get_power_keyboard)
    except PowerControlError as exc:
        await callback.message.edit_text(f"⚠️ {exc}", reply_markup=get_power_keyboard)


async def _send_capture(
    callback: CallbackQuery, status: str, capture: Callable[[], Path], media_type: str
) -> None:
    """Run a local capture without blocking updates, then deliver it to the admin."""
    await callback.answer()
    await callback.message.edit_text(status)
    captured_file: Path | None = None
    try:
        captured_file = await asyncio.to_thread(capture)
        media = FSInputFile(captured_file)
        if media_type == "photo":
            await callback.message.answer_photo(media, caption="📸 Знімок екрана")
        else:
            await callback.message.answer_audio(media, caption="🎙 Аудіозапис")
        await callback.message.edit_text("✅ Готово. Файл надіслано.")
    except MediaCaptureError as exc:
        await callback.message.edit_text(f"⚠️ {exc}")
    except Exception:
        await callback.message.edit_text("⚠️ Неочікувана помилка під час захоплення медіа.")
    finally:
        if captured_file:
            captured_file.unlink(missing_ok=True)
