from database import Base
from sqlalchemy import Column, Integer, Boolean, String, Text
from database import Session, engine
from dotenv import load_dotenv
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash, check_password_hash
from fantasy_application.src.auth.auth_helper import AuthHelper, AuthJWT
from fastapi.exceptions import HTTPException

load_dotenv()
session = Session(bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=False)
    referral_code = Column(String(8), nullable=True)
    winning_amount = Column(Integer, default=0)
    bonus_amount = Column(Integer, default=0)
    total_balance = Column(Integer, default=0)
    is_aadhar_verified = Column(Boolean, default=False)
    is_above_18 = Column(Boolean, default=True)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    @classmethod
    def get_user_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).first()

    @classmethod
    def create_user_object(cls, User, username, email, password, is_active,
                           is_staff, is_referral_valid=False,
                           ):
        bonus_amount = 100 if is_referral_valid else 0
        ref_code = AuthHelper.generate_referal_code()
        return User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_active=is_active,
            is_staff=is_staff,
            referral_code=ref_code,
            bonus_amount=bonus_amount,
            winning_amount=0,
            total_balance=bonus_amount,
            is_aadhar_verified=False,
            is_above_18=True,

        )

    @classmethod
    def commit_add_user_object(cls, user_object):
        session.add(user_object)
        session.commit()

    @classmethod
    def commit_user_object(cls):
        session.commit()

    @classmethod
    def user_exist_validation(cls, User, columns, schema_key):

        return User.get_user_by_column(columns, schema_key)

    @classmethod
    def user_credential_validation(cls, db_user, user, Authorize: AuthJWT = Depends()):
        if db_user and check_password_hash(db_user.password, user.password):
            access_token = Authorize.create_access_token(subject=db_user.username)
            refresh_token = Authorize.create_refresh_token(subject=db_user.username)

            response = {
                "access": access_token,
                "refresh": refresh_token
            }

            return jsonable_encoder(response)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Username Or Password"
                            )

    @classmethod
    def check_if_user_is_staff(cls, user):
        if not user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not a staff user"
            )

    @classmethod
    def update_user_as_per_schema(cls, user, username, email):
        user.username = username
        user.email = email
