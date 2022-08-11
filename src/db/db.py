import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.config.settings import DATABASE_URI, APPS_MODELS


# TORTOISE_ORM = {
#     "connections": {"default": DATABASE_URI},
#     "apps": {
#         "models": {
#             "models": ["src.app.users.models", "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=DATABASE_URI,
        modules={"models": APPS_MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
