"""Main file to run the FastAPI app."""

import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from routers import medias, tweets, users

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(medias.router)


@app.get("/")
async def root():
    """Root endpoint.

    Returns:
        JSON: {"message": "Hello world"}
    """
    return JSONResponse(
        content=jsonable_encoder({"message": "Hello world"}),
        status_code=status.HTTP_200_OK,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host="127.0.0.1")
