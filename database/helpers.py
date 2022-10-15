from .database import SessionLocal
from . import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def populate_db():
    db = SessionLocal()
    num_users = db.query(models.User).count()
    if num_users == 0:
        users = [{"username": "admin", "hashed_password": "password"}]
        
        for user in users:
            db.add(models.User(**user))
        
        db.commit()
    
    else:
        print(f"Database started, {num_users} users found")