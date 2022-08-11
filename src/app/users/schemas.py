from typing import Optional, Union
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User


class UserBase(BaseModel):
    """ user base scheme
    """
    id: int
    first_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    is_company: Optional[bool]


class UserInDB(UserBase):
    """ Custom user scheme
    """
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    avatar: Optional[str]

    class Config:
        orm_mode = True


# class UserCreate(UserInDB):
#     """ Свойства для получения через API при создании из админки
#     """
#     username: str
#     email: EmailStr
#     password: str
#     first_name: str
#     avatar: str = None


class UserCreateInRegistration(BaseModel):
    """ Create user in registration
    """
    username: str
    email: EmailStr
    password: str
    first_name: str
    avatar: Union[UploadFile, str] = None

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                email: EmailStr = Form(...),
                password: str = Form(...),
                first_name: str = Form(...),
                avatar: UploadFile = File(None)
                ):
        return cls(username=username, email=email, password=password, first_name=first_name, avatar=avatar)

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """ Properties to receive via API on update
    """
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_company: Optional[bool] = False
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """ Register admin scheme
    """
    username: str
    email: EmailStr
    password: str
    first_name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    is_company: Optional[bool] = True


class UserPublic(UserBase):
    """ For public profile user
    """

    class Config:
        orm_mode = True


User_C_Pydantic = pydantic_model_creator(
    User, name='create_user', exclude_readonly=True, exclude=('is_active', 'is_staff', 'is_superuser')
)
User_G_Pydantic = pydantic_model_creator(User, name='user')
