import jwt

from jwt import PyJWTError
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from src.config import settings
from src.app.users import service
from src.app.companies.models import Company
from src.app.users.models import User

from .jwt import ALGORITHM
from .schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)):
    """ Check auth user
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await service.user_s.get_obj(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


def get_user(current_user: User = Security(get_current_user)):
    """ Checking whether the user is active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_superuser(current_user: User = Security(get_current_user)):
    """ Checking whether the user is superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="User does not have enough privileges")
    return current_user


def get_company(current_user: User = Security(get_current_user)):
    """ Checking whether the user is company
    """
    if not current_user.is_company:
        raise HTTPException(status_code=400, detail="User does not have privileges of company")
    return current_user


async def get_author_user(
        request: Request,
        pk: int,
        current_user: User = Depends(get_company)
):
    """ Checking whether the user is author of resources
    """
    privileges_exist = False
    tags_of_route = request.scope['route'].tags
    if settings.TagName.COMPANY.value in tags_of_route:
        privileges_exist = await Company.filter(pk=pk, owner=current_user).exists()
    elif settings.TagName.ADDRESS.value in tags_of_route:
        privileges_exist = await Company.filter(addresses=pk, owner=current_user).exists()
    elif settings.TagName.VACANCY.value in tags_of_route:
        privileges_exist = await Company.filter(vacancies=pk, owner=current_user).exists()
    if not privileges_exist:
        raise HTTPException(status_code=400, detail="User is not an author of object")
    return current_user
