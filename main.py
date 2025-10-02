# from typing import Optional
# from fastapi import FastAPI, status, Response
# from enum import Enum
from fastapi import FastAPI, Request
from router import users,  otp
from auth import authentication
from models import user
from db.database import engine, Base
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from router import users


app = FastAPI()

app.include_router(users.router, prefix = '/user', tags = ['user'])
app.include_router(otp.router, prefix = '/otp', tags = ['otp'])
app.include_router(authentication.router)

Base.metadata.create_all(engine)

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


