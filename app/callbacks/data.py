from aiogram.types import CallbackQuery, Message
from aiogram import Router, F

class CallbacksManager:
    @staticmethod
    def get():
        callbacks_data = [
            "start_administration",
            "start_configuration",
            "admin_menu",
            "admin_status",
            "admin_info",
            "capture_screenshot",
            "capture_audio",
            "admin_download",
            "power_menu",
            "power_shutdown_confirm",
            "power_shutdown_0",
            "power_shutdown_300",
            "power_shutdown_900",
            "power_shutdown_1800",
            "power_lock",
            "power_abort",
            "config_logs",
            "config_logs_message",
            "config_logs_file",
            "config_top_memory",
            "send_notification",
            "send_command",
            "notification_cancel",
            "end_configuration",
            "command_cancel"
        ]
        return callbacks_data
