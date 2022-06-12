from telegram.ext import Updater

from src.core.config import settings
from src.telegram.handlers.help_handler import help_command
from src.telegram.handlers.schedule_handler import get_handler

handlers = [help_command, get_handler]


def main() -> None:
    updater = Updater(token=settings.telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    [dispatcher.add_handler(handler) for handler in handlers]

    updater.start_polling()
    updater.idle()
