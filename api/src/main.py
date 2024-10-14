import os
import sys

import uvicorn
from fastapi import FastAPI

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.routers import users
from src.routers import tweets, medias


app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(medias.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host="127.0.0.1")
