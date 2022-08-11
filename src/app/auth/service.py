import jwt

from jwt import InvalidTokenError
from datetime import datetime, timedelta
from tortoise.expressions import Q
from typing import Optional
from enum import Enum

from src.app.users import models, service
from src.config import settings
from src.app.users import schemas
from src.app.auth.celery_worker import send_register_email

from .models import Verification
from .schemas import VerificationOut

password_reset_jwt_subject = "preset"


class UserType(str, Enum):
    """ Type of user for registration
    """
    user = "user"
    company = "company"


async def registration_user(
        new_user: schemas.UserCreateInRegistration, user_type: UserType,
) -> bool:
    """ User Registration
    """
    if await models.User.filter(Q(username=new_user.username) | Q(email=new_user.email)).exists():
        return True
    else:
        if user_type == UserType.company:
            user = await service.user_s.create_user(new_user, is_company=True)
        else:
            user = await service.user_s.create_user(new_user)
        verify = await Verification.create(user_id=user.id)
        send_register_email.delay(new_user.email, new_user.username, new_user.password, verify.link)
        return False


async def verify_registration_user(uuid: VerificationOut) -> bool:
    """ Confirmation of the user's email
    """
    verify = await Verification.get(link=uuid.link).select_related("user")
    if verify:
        await service.user_s.update(
            schema=schemas.UserUpdate(**{"is_active": "true"}), id=verify.user.id
        )
        await Verification.filter(link=uuid.link).delete()
        return True
    else:
        return False


def generate_password_reset_token(email: str):
    """ Generating a password reset token
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """ Check the password reset token
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None
