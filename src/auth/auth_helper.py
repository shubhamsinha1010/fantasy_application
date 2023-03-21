import smtplib
from email.message import EmailMessage

from fastapi import status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import string
import random

load_dotenv()

class AuthHelper:
    @staticmethod
    def user_token_authenticator(Authorize:AuthJWT = Depends()):
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token") from e

    @staticmethod
    def generate_referal_code(n):
        return ''.join(random.choices(string.ascii_letters, k=n))

    @staticmethod
    def send_email(User,username,email_address,email_password):
        try:
            msg = EmailMessage()
            user = User.get_user_by_column(User.username, username)
            msg['Subject'] = "FantasySports11 authentication code"
            msg['From'] = email_address
            msg['To'] = user.email  # type Email
            auth_code = AuthHelper.generate_referal_code(16)
            msg.set_content(
                f"""\
                Hello {user.username}, Welcome to FantasySports11 , Your authentication code is {auth_code}.
            """)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                user.auth_code = auth_code
                from fantasy_application.src.auth.models import session
                session.commit()
                smtp.login(email_address, email_password)
                smtp.send_message(msg)

        except Exception as e:
            raise Exception(f"Error occurred due to {e}")
