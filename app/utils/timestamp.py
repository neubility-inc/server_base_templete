from datetime import datetime
from pytz import timezone


class TimeStamp:
    def __init__(self, zone: str = "Asia/Seoul") -> None:
        self.zone: str = zone
        self.time = None

    def get_current_time(self):
        self.time = datetime.now(timezone(self.zone))
        return self.time

    def get_current_utc_time(self):
        return datetime.now(timezone("UTC"))

    def get_current_time_to_format(self, format):
        return datetime.now(timezone(self.zone)).strftime(format)


timestamp = TimeStamp()
