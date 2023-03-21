from pydantic import BaseModel
from dotenv import load_dotenv
import os
from database import Base,engine
from fastapi_mail import ConnectionConfig
from fantasy_application.src.auth.models import User
from fantasy_application.src.contest.models import Contest

load_dotenv()



class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")


conf = ConnectionConfig(
    MAIL_USERNAME ="sinhashubham1911",
    MAIL_PASSWORD = "bayaxiumjrkrgaqd",
    MAIL_FROM = "sinhashubham1911@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "mail server",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


print("Creating database ....")

Base.metadata.create_all(engine)