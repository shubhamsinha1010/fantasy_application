from fastapi import status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv

load_dotenv()
import string
import random




class AuthHelper:
    @staticmethod
    def user_token_authenticator(Authorize:AuthJWT = Depends()):
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token") from e

    @staticmethod
    def generate_referal_code():
        return ''.join(random.choices(string.ascii_letters, k=8))
