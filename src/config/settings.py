import os

from .local_config import *

from enum import Enum

PROJECT_NAME = "Interviews"
SERVER_HOST = "https://127.0.0.1:8000"

SECRET_KEY = b"awubsyb872378t^*TG8y68&*&&*8y8yg9POB)*896ft7CR^56dfYUv"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_V1_STR = "/api/v1"

# Token 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
]

DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER", POSTGRES_USER)}:' \
               f'{os.environ.get("POSTGRES_PASSWORD", POSTGRES_PASSWORD)}@' \
               f'{os.environ.get("POSTGRES_HOST", POSTGRES_HOST)}:5432/' \
               f'{os.environ.get("POSTGRES_DB", POSTGRES_DB)}'

# TESTING = False

USERS_OPEN_REGISTRATION = True

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "src/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_NAME
EMAIL_TEST_USER = 'test@maio.ru'


class TagName(Enum):
    """ Check tag name for permissions
    """
    VACANCY = 'vacancy'
    COMPANY = 'company'
    ADDRESS = 'address'


APPS_MODELS = [
    "src.app.reviews.models",
    "src.app.vacancies.models",
    "src.app.companies.models",
    "src.app.users.models",
    "src.app.auth.models",
    "aerich.models"
]

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
