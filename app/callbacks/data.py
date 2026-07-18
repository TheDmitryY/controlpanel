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
            "admin_info"
        ]
        return callbacks_data
