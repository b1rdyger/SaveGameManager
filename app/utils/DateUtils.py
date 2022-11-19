import datetime

class DateUtils:
    @staticmethod
    def get_formated_time(dt):
        return datetime.datetime.strftime(dt, "%d.%m. %H:%M")
