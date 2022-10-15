from typing import Union
from fastapi import FastAPI
import uvicorn

from accounts.accounts import accountroute, accountprefix

app = FastAPI()
app.include_router(accountroute, prefix=accountprefix)

@app.get("/")
async def read_root():
    return {"service": "main", "status": "Healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)