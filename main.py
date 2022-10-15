from typing import Union
from fastapi import FastAPI
import uvicorn


from accounts.accounts import accountroute, accountprefix
from database import models
from database.database import SessionLocal, engine
from database.helpers import populate_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(accountroute, prefix=accountprefix)

@app.on_event("startup")
def startup_populate_db():
    populate_db()
    
@app.get("/")
async def read_root():
    return {"service": "main", "status": "Healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)