from datetime import date, datetime


class SheduleBaseService:
    def __init__(self) -> None:
        pass

    def get_schedule(
        group_name: str, date_: date, datetime_: datetime, by_group: bool = False
    ) -> dict:
        """Search schedule by group name"""
        raise NotImplementedError

    def get_group_name(student_reg_number: int) -> str:
        raise NotImplementedError
