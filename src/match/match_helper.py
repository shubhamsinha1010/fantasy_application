from datetime import datetime

import schedule,time

class MatchHelper:

    @staticmethod
    def calculate_time_left(date_time):
        dt2 = datetime.now()
        dt1 = datetime.strptime(date_time, "%d/%m/%y %H:%M")

        diff = (dt1 - dt2).total_seconds()
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

    @staticmethod
    def change_match_status():
        from fantasy_application.src.match.models import Match
        match_list = Match.get_match_list()
        for match in match_list:
            dt1 = datetime.now()
            dt2 = match.deadline
            diff = (dt1 - dt2).total_seconds()
            if diff > 0:
                match.is_match_open = False
                Match.commit_match_object()

    @staticmethod
    def run_job():
        schedule.every(5).seconds.do(MatchHelper.change_match_status)
        while True:
            schedule.run_pending()
            time.sleep(1)


