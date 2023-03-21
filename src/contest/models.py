from fastapi.encoders import jsonable_encoder

from database import Base, Session, engine
from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime
from fantasy_application.src.contest.contest_helper import ContestHelper

session = Session(bind=engine)


class Contest(Base):
    __tablename__ = 'contest'
    id = Column(Integer, primary_key=True)
    team_1 = Column(String(50),nullable=False)
    team_2 = Column(String(50),nullable=False)
    series_name = Column(Text,nullable=False)
    has_mega_contest = Column(Boolean,nullable=False)
    is_contest_open = Column(Boolean,nullable=False,default=True)
    deadline = Column(DateTime)



    @classmethod
    def create_contest_object(cls, Contest, team_1, team_2, series_name, has_mega_contest, is_contest_open, deadline):
        return Contest(
            team_1=team_1,
            team_2=team_2,
            series_name=series_name,
            has_mega_contest=has_mega_contest,
            is_contest_open=is_contest_open,
            deadline=deadline
        )

    @classmethod
    def commit_add_contest_object(cls, contest_object,contest):
        hours,minutes = ContestHelper.calculate_time_left(contest.deadline)
        session.add(contest_object)
        session.commit()
        response = {
            "team_1": contest_object.team_1,
            "team_2": contest_object.team_2,
            "series_name": contest_object.series_name,
            "has_mega_contest": contest_object.has_mega_contest,
            "is_contest_open": contest_object.is_contest_open,
            "time_left": f"{hours}hrs {minutes}mins"
        }

        return jsonable_encoder(response)

    @classmethod
    def commit_contest_object(cls):
        session.commit()