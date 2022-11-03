# Used for importing models from database -> python doesn't import from parent directories
import sys
from database.helpers import get_async_session

sys.path.append("..")

# Imports
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status

from fastapi_another_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

# Helper functions
from accounts.helpers import *

authprefix = "/auth"
authroute = APIRouter()


@authroute.get("/")
def health():
    return {"service": "auth", "status": "Healthy"}


@authroute.post("/register")
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_async_session),
    Authorize: AuthJWT = Depends(),
):
    registerUsername = form_data.username
    registerPassword = form_data.password
    result = await new_user(registerUsername, registerPassword, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Registration unsuccessful"
        )

    access_token = Authorize.create_access_token(subject=result.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=result.username)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {
        "user": result.username,
        "token_type": "bearer",
    }


@authroute.post(
    "/login",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_async_session),
    Authorize: AuthJWT = Depends(),
):
    loginUsername = form_data.username
    loginPassword = form_data.password
    result = await validate_user(username=loginUsername, password=loginPassword, db=db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = Authorize.create_access_token(subject=result.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=result.username)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    
    return {
        "user": result.username,
        "token_type": "bearer",
    }


@authroute.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@authroute.delete("/logout")
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@authroute.get("/protected")
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


# Only fresh JWT access token can access this endpoint
@authroute.get("/protected-fresh")
def protected_fresh(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
