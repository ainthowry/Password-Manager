from fastapi import FastAPI, Request
from pydantic import BaseModel
import databases

from database.database import SQLALCHEMY_DATABASE_URL
from database.helpers import create_db_and_tables

from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Routes
from accounts.accounts import accountroute, accountprefix
from auth.auth import authroute, authprefix

from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accountroute, prefix=accountprefix)
app.include_router(authroute, prefix=authprefix)

database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.on_event("startup")
async def startup():
    # No migration currently begin used
    await create_db_and_tables()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"service": "main", "status": "Healthy"}


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = False
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = True
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
