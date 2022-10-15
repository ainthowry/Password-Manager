from fastapi import APIRouter
from database.classes import Account

accountprefix = '/accounts'
accountroute = APIRouter()

@accountroute.get('/')
def status():
    return {"service": "accounts", "status": "Healthy"}
    
@accountroute.get('/login')
def login(loginInput: Account):
    return loginInput

@accountroute.post('/register')
def register(registerInput: Account):
    return registerInput
    
@accountroute.post('/change')
def change(loginInput: Account, newPassword: str):
    return loginInput, newPassword
    

@accountroute.get('/subaccount')
def subaccount(loginInput: Account):
    return loginInput