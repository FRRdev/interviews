from fastapi import APIRouter, Body, Depends, HTTPException, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette.templating import Jinja2Templates

from src.app.users import schemas, service

from .celery_worker import send_recover_email
from .schemas import Token, Msg, VerificationOut
from .jwt import create_token
from .service import (
    generate_password_reset_token,
    verify_password_reset_token,
    registration_user,
    verify_registration_user,
    UserType
)

auth_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@auth_router.post("/login/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ OAuth2 compatible token login, get an access token for future requests
    """
    user = await service.user_s.authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_token(user.id)


@auth_router.post("/registration", response_model=Msg)
async def user_registration(
        new_user: schemas.UserCreateInRegistration = Depends(schemas.UserCreateInRegistration.as_form),
        user_type: UserType = Query(...),
):
    """ User_registration
    """
    user = await registration_user(new_user, user_type)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return {"msg": "Send email"}


@auth_router.post("/confirm-email", response_model=Msg)
async def confirm_email(uuid: VerificationOut):
    """ Confirm email to set is_active=True
    """
    if await verify_registration_user(uuid):
        return {"msg": "Success verify email"}
    else:
        raise HTTPException(status_code=404, detail="Not found")


@auth_router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(email: str):
    """ Password Recovery
    """
    user = await service.user_s.get_obj(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email)
    send_recover_email.delay(email_to=user.email, email=email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@auth_router.post("/reset-password/", response_model=Msg)
async def reset_password(token: str = Body(...), new_password: str = Body(...)):
    """ Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await service.user_s.get_obj(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    await service.user_s.change_password(user, new_password)
    return {"msg": "Password updated successfully"}
