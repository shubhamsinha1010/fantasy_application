from http.client import HTTPException
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from fantasy_application.src.auth.auth_helper import AuthHelper
from fantasy_application.src.contest.contest_helper import ContestHelper
from fantasy_application.src.auth.models import User
from fantasy_application.src.contest.models import Contest
from fantasy_application.src.contest.schemas import ContestAddSchema

contest_router = APIRouter(
    prefix='/contest',
    tags=['auth']

)


@contest_router.post('/add-contest', status_code=201)
async def add_contest(contest: ContestAddSchema, Authorize:AuthJWT=Depends()):
    """
    Api to add a contest by staff user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username = Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a staff user"
        )
    if ContestHelper.is_time_less_than_current(contest.deadline):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Date for the contest is less than the current time"
        )

    datetime_object = ContestHelper.convert_str_to_datetime(contest.deadline)
    contest_object = Contest.create_contest_object(Contest,contest.team_1,contest.team_2,
                                                   contest.series_name, contest.has_mega_contest,
                                                   contest.is_contest_open, datetime_object)


    return Contest.commit_add_contest_object(contest_object,contest)





