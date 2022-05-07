from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def _help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text(
        "Используйте /start для запуска функционала бота."
    )


help_command = CommandHandler("help", _help_command)
