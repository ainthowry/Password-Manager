#Used for importing models from database -> python doesn't import from parent directories
import sys
sys.path.append("..")

#Imports
from fastapi import Depends, APIRouter
from database.classes import Account
from database.helpers import get_db
from sqlalchemy.orm import Session

#Db models
from database import models

accountprefix = '/accounts'
accountroute = APIRouter()

@accountroute.get('/')
def status():
    return {"service": "accounts", "status": "Healthy"}
    
@accountroute.get('/login')
def login(db: Session = Depends(get_db)):
    owner = db.query(models.User).all()
    print(owner)
    return owner

@accountroute.post('/register')
def register(registerInput: Account, db: Session = Depends(get_db)):
    owner = db.query(models.User).all()
    print(owner)
    return registerInput
    
@accountroute.post('/change')
def change(loginInput: Account, newPassword: str):
    return loginInput, newPassword
    

@accountroute.get('/subaccount')
def subaccount(loginInput: Account):
    return loginInput