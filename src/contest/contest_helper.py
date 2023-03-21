from datetime import datetime


class ContestHelper:

    @staticmethod
    def calculate_time_left(date_time):
        dt2 = datetime.now()
        dt1 = datetime.strptime(date_time, "%d/%m/%y %H:%M")
        diff = (dt2 - dt1).total_seconds()
        hours = diff // 3600
        minutes = (diff % 3600) // 60
        return hours, minutes

    @staticmethod
    def convert_str_to_datetime(date_time):
        return datetime.strptime(date_time, "%d/%m/%y %H:%M")

    @staticmethod
    def is_time_less_than_current(date_time):
        dt2 = datetime.now()
        dt1 = datetime.strptime(date_time, "%d/%m/%y %H:%M")
        diff = (dt2 - dt1).total_seconds()
        return diff > 0

