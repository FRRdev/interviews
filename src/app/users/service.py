import aiofiles

from typing import Optional
from fastapi import HTTPException, UploadFile
from tortoise.expressions import Q
from uuid import uuid4

from . import schemas, models
from ..base.base_service import BaseService
from src.app.auth.security import verify_password, get_password_hash


class UserService(BaseService):
    model = models.User
    create_schema = schemas.UserCreateInRegistration
    update_schema = schemas.UserUpdate
    get_schema = schemas.User_G_Pydantic

    async def create_user(self, schema: schemas.UserCreateInRegistration, **kwargs):
        file_name = f'media/{schema.username}_{uuid4()}.jpeg' if schema.avatar else None
        if file_name:
            if schema.avatar.content_type == "image/jpeg":
                await UserService.write_user_image(file_name, schema.avatar)
            else:
                raise HTTPException(status_code=418, detail='It is not jpeg')
        hash_password = get_password_hash(schema.dict().pop("password"))
        return await self.create(
            schemas.UserCreateInRegistration(
                **schema.dict(exclude={"password", "avatar"}), password=hash_password, avatar=file_name, is_active=False
            ), **kwargs
        )

    @staticmethod
    async def write_user_image(file_name: str, file: UploadFile):
        async with aiofiles.open(file_name, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)

    async def update_user(self, schema: schemas.UserUpdate, **kwargs):
        hash_password = get_password_hash(schema.dict().pop("password"))
        return await self.update(
            schemas.UserUpdate(
                **schema.dict(exclude={"password"}), password=hash_password
            ), **kwargs
        )

    async def authenticate(self, username: str, password: str) -> Optional[model]:
        user = await self.model.get(username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def change_password(self, obj: models.User, new_password: str):
        hashed_password = get_password_hash(new_password)
        obj.password = hashed_password
        await obj.save()

    async def get_username_email(self, username: str, email: str):
        return await self.model.get_or_none(Q(username=username) | Q(email=email))

    async def create_superuser(self, schema: schemas.UserCreateInRegistration):
        hash_password = get_password_hash(schema.dict().pop("password"))
        return await self.create(
            schemas.UserCreate(
                **schema.dict(exclude={"password"}),
                password=hash_password,
                is_active=True,
                is_superuser=True,
                is_company=True
            )
        )


user_s = UserService()
