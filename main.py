from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fantasy_application.src.match.match_helper import MatchHelper
from fantasy_application.src.auth.router import auth_router
from fantasy_application.src.match.router import match_router
from fantasy_application.src.config import Settings
import multiprocessing

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(match_router)


if __name__ == '__main__':
    process = multiprocessing.Process(target=MatchHelper.run_job())
    process.start()
