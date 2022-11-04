# Used for importing models from database -> python doesn't import from parent directories
import sys
from database.helpers import get_async_session

sys.path.append("..")

# Imports
from fastapi import Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_another_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

# Helper functions
from .helpers import *

# Db models
from database import models

accountprefix = "/accounts"
accountroute = APIRouter()

# Generate secret_key

# GetAllSubAccounts -> subaccount.id, subaccount.name, subaccount.username
# GetSubAccount
# CreateSubAccount
# DeleteSubAccount


@accountroute.get("/")
def health():
    return {"service": "accounts", "status": "Healthy"}


@accountroute.post("/change")
async def change(
    newPassword: str = Form(),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_async_session),
):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    result = await update_password(
        username=current_user, newPassword=newPassword, db=db
    )
    return result


@accountroute.get("/subaccount")
async def findSubaccount(id:str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_async_session),):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    result = await get_subaccount(id, current_user, db)
    return result


@accountroute.get("/subaccounts")
async def findSubaccounts(Authorize: AuthJWT = Depends(), db: Session = Depends(get_async_session),):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    result = await get_subaccounts(current_user, db)

    return result


@accountroute.post("/create/subaccount")
async def createSub(
    form_data: OAuth2PasswordRequestForm = Depends(),
    name: str = Form(),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_async_session),
):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    new_subAccount = subaccountDetails()
    new_subAccount.name = name
    new_subAccount.subUsername = form_data.username
    new_subAccount.subPassword = form_data.password

    result = await create_subaccount(
        username=current_user, subaccount_details=new_subAccount, db=db
    )

    return current_user, result
