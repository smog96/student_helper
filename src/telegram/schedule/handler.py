from enum import Enum
from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
)


class _States(Enum):
    FIRST = 1
    SECOND = 2


def _start(update: Update, context: CallbackContext):
    """
    1. check if user in db
        a. if user not in db:
            - go to search by reg_num or group_name
        b. if user exist:
            - ask about date (now, tomorrow or different date (datetime))
    """
    user = update.message.from_user


def get_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", _start)],
        states={},
        fallbacks=[CommandHandler("start", _start)],
    )
