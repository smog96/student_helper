from src.repositories.telegram_repository import TelegramRepository


class TelegramService:
    def __init__(self) -> None:
        self.repository = TelegramRepository()
