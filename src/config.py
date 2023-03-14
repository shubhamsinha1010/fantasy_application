from pydantic import BaseModel
from dotenv import load_dotenv
import os
from database import Base,engine

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")




print("Creating database ....")

Base.metadata.create_all(engine)