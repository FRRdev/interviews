import os

from fastapi import FastAPI

from src.db.db import init_db
from src.config import settings
from src.app import routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles


def create_application() -> FastAPI:
    application = FastAPI(
        title="Interviews",
        description="Author - FRRDev",
        version="0.1.0",
    )
    return application


app = create_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(routers.api_router, prefix=settings.API_V1_STR)
app.mount("/media", StaticFiles(directory="media"), name="media")
add_pagination(app)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
