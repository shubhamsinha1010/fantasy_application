from fastapi import APIRouter, status, Depends
from .schemas import SignUpSchema, LoginSchema
from fantasy_application.src.auth.models import User
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from .auth_helper import AuthHelper
from fastapi.exceptions import HTTPException

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']

)


@auth_router.post('/signup', status_code=201)
async def signup(user: SignUpSchema):
    """
    Api to login a particular user
    """
    email_exists = User.user_exist_validation(User,User.email,user.email)
    username_exists = User.user_exist_validation(User,User.username,user.username)
    if email_exists or username_exists:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="User already exists"
                                 )
    if not user.is_above_18:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                             detail="User cannot be registered as the minimum age to use the app is 18"
                             )
    is_referral_valid = False
    if user.friend_referal_code:

        is_valid_code = User.get_user_by_column(User.referral_code,user.friend_referal_code)
        if is_valid_code:
            is_referral_valid = True

    new_user = User.create_user_object(User,username=user.username,email=user.email,
                                       password=user.password,is_active=user.is_active,
                                       is_staff=user.is_staff,
                                       is_referral_valid = is_referral_valid
                                       )

    User.commit_add_user_object(new_user)
    return {col.name: getattr(new_user, col.name) for col in new_user.__table__.columns}

@auth_router.post('/login', status_code=200)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    """
    Api to login a particular user
    """
    db_user = User.get_user_by_column(User.username, user.username)
    return User.user_credential_validation(db_user, user, Authorize)





# refreshing tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    Api to  create a fresh token. It requires an refresh token.
    """
    AuthHelper.user_token_authenticator(Authorize)
    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})