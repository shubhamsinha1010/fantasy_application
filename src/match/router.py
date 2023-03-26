from http.client import HTTPException
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fantasy_application.src.auth.auth_helper import AuthHelper
from fantasy_application.src.match.match_helper import MatchHelper
from fantasy_application.src.auth.models import User
from fantasy_application.src.match.models import Match
from fantasy_application.src.match.schemas import MatchAddSchema, MatchUpdateSchema

match_router = APIRouter(
    prefix='/match',
    tags=['match']

)


@match_router.post('/add-match', status_code=201)
async def add_match(match: MatchAddSchema, Authorize: AuthJWT = Depends()):
    """
    Api to add a match by staff user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username = Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a staff user"
        )
    if MatchHelper.is_time_less_than_current(match.deadline):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Date for the match is less than the current time"
        )

    datetime_object = MatchHelper.convert_str_to_datetime(match.deadline)
    match_object = Match.create_match_object(Match, match.team_1, match.team_2,
                                                   match.series_name, match.has_mega_contest,
                                                   match.is_match_open, datetime_object)

    return Match.commit_add_match_object(match_object, match)


@match_router.get('/get-scores', status_code=200)
async def add_match():
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        "X-RapidAPI-Key": "efeeef677cmshae5edb65a989979p185378jsnd6957fa89188",
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    response = response.json()

    return response


@match_router.patch('/update-deadline/{id}', status_code=200)
async def add_contest(id:int,match_update:MatchUpdateSchema, Authorize: AuthJWT = Depends()):
    """
    Api to update a match
    """
    AuthHelper.user_token_authenticator(Authorize)
    username = Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a staff user"
        )
    match = Match.get_match_by_column(Match.id, id)
    if match_update.deadline:
        match.deadline=match_update.deadline

    if match_update.is_match_open:
        match.is_match_open=match_update.is_match_open

    Match.commit_match_object()
    response = {
        "deadline": match.deadline,
        "is_match_open": match.is_match_open
    }
    return jsonable_encoder(response)

