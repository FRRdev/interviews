from typing import List

from fastapi import APIRouter, Depends
from src.app.users.models import User
from src.app.auth.permissions import get_superuser, get_user
from .. import schemas, service

skill_router = APIRouter()


@skill_router.post('/', response_model=schemas.GetSkill)
async def create_skill(
        schema: schemas.CreateSkill,
        user: User = Depends(get_superuser)
):
    """ Create skill router
    """
    return await service.skill_s.create(schema)


@skill_router.get('/', response_model=List[schemas.GetSkill])
async def get_list_skills(user: User = Depends(get_user)):
    """ Get skill's list router
    """
    return await service.skill_s.all()


@skill_router.delete('/{pk}', status_code=204)
async def delete_skill(pk: int, user: User = Depends(get_superuser)):
    """ Delete skill
    """
    return await service.skill_s.delete(id=pk)
