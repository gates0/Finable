# from typing import Optional
# from fastapi import FastAPI, status, Response
# from enum import Enum
from fastapi import FastAPI, Request
from router import user
from auth import authentication
from db import models
from db.database import engine
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

origins = [
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ['*']
)


