import time
from enum import Enum
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    filters,
    Filters,
)

from src.core.config import settings, logger
from src.repositories.telegram_repository import TelegramRepository
from src.repositories.user_repository import UserRepository
from src.schemas.telegram_user import TelegramCreate
from src.services.student_service import StudentAPIService


class Routes(str, Enum):
    ACQUAINTANCE = "acquaintance"
    REGISTRATION = "registration"
    REGISTRATION_NUMBER = "reg_number"
    MAIN = "main"
    SCHEDULE = "schedule"


class RegistrationStates(str, Enum):
    PORTAL = "portal_data"
    REG_NUMBER = "student_reg_number"


class MainStates(str, Enum):
    MAIN = "main"
    GO_SCHEDULE = "go_schedule"
    # etc


class ScheduleStates(str, Enum):
    TODAY = "today"
    TOMORROW = "tomorrow"


class TelegramHandler:
    def __init__(self):
        self.tg_repo = TelegramRepository()
        self.user_repo = UserRepository()
        self.student_service = StudentAPIService(
            base_url="api.portal.ru",
            api_login="login",
            api_password="pwd",
            ssl_secure=True,
        )

    def start(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        is_exist = self.tg_repo.check_exist(tg_user=user)

        if is_exist is False:
            return self.acquaintance(update, context)
        return self.main_choice(update, context)

    # --- Registration zone

    def acquaintance(self, update: Update, context: CallbackContext):
        """знакомство с пользователем"""
        keyboard = [
            [
                InlineKeyboardButton(
                    "Поиск по порталу",
                    callback_data=RegistrationStates.PORTAL,
                ),
            ],
            [
                InlineKeyboardButton(
                    "Поиск по зачётке",
                    callback_data=RegistrationStates.REG_NUMBER,
                ),
            ],
        ]
        update.message.reply_text(
            f"Мы с Вами ещё не знакомы. Найдём Вас в базе {settings.university_name}?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return Routes.REGISTRATION

    def find_api_data(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.edit_message_text("Отлично, сейчас поищу в базе")
        time.sleep(3)
        # todo: find user
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=MainStates.MAIN),
                InlineKeyboardButton("Нет", callback_data=RegistrationStates.REG_NUMBER),
            ]
        ]
        query.edit_message_text(
            "Нашел пользователя {Бурдасов Илья}. Верно?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return Routes.MAIN

    def find_student_reg_number(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.edit_message_text("Отлично, мне нужен номер Вашей зачётки")
        return Routes.REGISTRATION_NUMBER

    def wrong_reg_number(self, update: Update, context: CallbackContext):
        update.message.reply_text("Введен неверный формат зачётки, новая попытка")
        return Routes.REGISTRATION_NUMBER

    def student_reg_number(self, update: Update, context: CallbackContext):
        # todo: find user
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=MainStates.MAIN),
                InlineKeyboardButton("Нет", callback_data=RegistrationStates.REG_NUMBER),
            ]
        ]
        update.message.reply_text(
            "Нашел пользователя {Бурдасов Илья}. Верно?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return Routes.MAIN

    # --- Main zone

    def _reg_number_(self, update: Update, msg: str):
        query = update.callback_query
        query.answer()
        query.edit_message_text("Необходимо ввести номер зачётки и я сохраню его")
        return Routes.REGISTRATION_NUMBER

    def return_to_reg_number(self, update: Update, context: CallbackContext):
        return self._reg_number_(update, "Необходимо ввести номер зачётки и я сохраню его")

    def change_reg_number(self, update: Update):
        return self._reg_number_(update, "Хорошо, готов сохранить другой номер")

    def main_choice(self, update: Update, context: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("Расписание", callback_data=MainStates.GO_SCHEDULE),
            ],
            [
                InlineKeyboardButton(
                    "Промежуточная успеваемость",
                    callback_data=MainStates.GO_SCHEDULE,  # todo
                ),
            ],
            [InlineKeyboardButton("Изменить номер зачётки", callback_data=RegistrationStates.REG_NUMBER)],
        ]
        msg = f"Привет, {update.effective_user.first_name}!"
        query = update.callback_query
        if query:
            query.answer()
            query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        return Routes.MAIN

    def go_to_schedule(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        keyboard = [
            [
                InlineKeyboardButton("Сегодня", callback_data=ScheduleStates.TODAY),
                InlineKeyboardButton("Завтра", callback_data=ScheduleStates.TOMORROW),
            ],
            # [ todo
            #     InlineKeyboardButton("Другая дата"),
            #     InlineKeyboardButton("Другая группа"),
            # ]
        ]
        query.edit_message_text(
            "Хорошо, теперь надо выбрать день",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        return Routes.SCHEDULE

    # --- Schedule zone

    def choice_day(self, update: Update, context: CallbackContext):
        pass

    # --- --- --- --- --- ---

    def get_handler(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                Routes.REGISTRATION: [
                    CallbackQueryHandler(
                        self.find_api_data,
                        pattern=rf"^{RegistrationStates.PORTAL}$",
                    ),
                    CallbackQueryHandler(
                        self.find_student_reg_number,
                        pattern=rf"^{RegistrationStates.REG_NUMBER}$",
                    ),
                ],
                Routes.REGISTRATION_NUMBER: [
                    MessageHandler(
                        Filters.regex(r"^[0-9]{6}$"),
                        self.student_reg_number,
                    ),
                    MessageHandler(Filters.text, self.wrong_reg_number),
                ],
                Routes.MAIN: [
                    CallbackQueryHandler(self.return_to_reg_number, pattern=rf"^{RegistrationStates.REG_NUMBER}"),
                    CallbackQueryHandler(self.main_choice, pattern=rf"^{MainStates.MAIN}$"),
                    CallbackQueryHandler(
                        self.go_to_schedule,
                        pattern=rf"^{MainStates.GO_SCHEDULE}$",
                    ),
                ],
                Routes.SCHEDULE: [],
            },
            fallbacks=[CommandHandler("start", self.start)],
        )


get_handler = TelegramHandler().get_handler()
