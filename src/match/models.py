from fastapi.encoders import jsonable_encoder

from database import Base, Session, engine
from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime
from fantasy_application.src.match.match_helper import MatchHelper

session = Session(bind=engine)


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    team_1 = Column(String(50),nullable=False)
    team_2 = Column(String(50),nullable=False)
    series_name = Column(Text,nullable=False)
    has_mega_contest = Column(Boolean,nullable=False)
    is_match_open = Column(Boolean,nullable=False,default=True)
    deadline = Column(DateTime)



    @classmethod
    def create_match_object(cls, Match, team_1, team_2, series_name, has_mega_contest, is_match_open, deadline):
        return Match(
            team_1=team_1,
            team_2=team_2,
            series_name=series_name,
            has_mega_contest=has_mega_contest,
            is_match_open=is_match_open,
            deadline=deadline
        )

    @classmethod
    def get_match_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).first()

    @classmethod
    def get_match_list(cls):
        return session.query(cls).filter(Match.is_match_open == True).all()

    @classmethod
    def commit_add_match_object(cls, match_object,match):
        hours,minutes = MatchHelper.calculate_time_left(match.deadline)
        session.add(match_object)
        session.commit()
        response = {
            "team_1": match_object.team_1,
            "team_2": match_object.team_2,
            "series_name": match_object.series_name,
            "has_mega_contest": match_object.has_mega_contest,
            "is_match_open": match_object.is_match_open,
            "time_left": f"{hours}hrs {minutes}mins"
        }

        return jsonable_encoder(response)

    @classmethod
    def commit_match_object(cls):
        session.commit()