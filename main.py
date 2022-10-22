from fastapi import FastAPI

import databases
import sqlalchemy

from database.database import SQLALCHEMY_DATABASE_URL, create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


from accounts.accounts import accountroute, accountprefix

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accountroute, prefix=accountprefix)
database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"service": "main", "status": "Healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
