from telegram.ext import Updater

from src.core.config import settings
from src.telegram.schedule.handler import get_handler as schedule_handler
from src.telegram.schedule.test_handl import conv_handler


def main() -> None:
    updater = Updater(token=settings.telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
