"""Main file to run the FastAPI app."""

import uvicorn
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from database_models.db_config import get_async_session

from routers import medias, tweets, users
from database_models.setup import setup_test_data

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(medias.router)


@app.get("/")
async def root(session: AsyncSession = Depends(get_async_session)):
    # await setup_test_data(session)
    return JSONResponse(
        content=jsonable_encoder({"message": "Hello world"}),
        status_code=status.HTTP_200_OK,
    )

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host="127.0.0.1")
