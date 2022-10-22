# Used for importing models from database -> python doesn't import from parent directories
import sys
from database.database import get_async_session

sys.path.append("..")

# Imports
from fastapi import Depends, APIRouter
from database.dto import Account, RegisterInput
from sqlalchemy.orm import Session

# Db models
from database import models

accountprefix = "/accounts"
accountroute = APIRouter()


@accountroute.get("/")
def status():
    return {"service": "accounts", "status": "Healthy"}


@accountroute.post(
    "/login",
)
def login(loginInput: Account, db: Session = Depends(get_async_session)):
    result = models.User(
        username=registerInput.username, password=registerInput.password
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return owner


@accountroute.post("/register")
def register(registerInput: RegisterInput, db: Session = Depends(get_async_session)):
    result = models.User(
        username=registerInput.username, password=registerInput.password
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@accountroute.post("/change")
def change(loginInput: Account, newPassword: str):
    return loginInput, newPassword


@accountroute.get("/subaccount")
def subaccount(loginInput: Account):
    return loginInput
