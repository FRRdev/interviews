from typing import List
from fastapi import APIRouter, Depends, Path

from .. import schemas, models, service
from src.app.auth.permissions import get_superuser, get_user

comment_router = APIRouter()


@comment_router.post('/{pk}', response_model=schemas.CommentBaseOut)
async def create_comment(
        schema: schemas.CreateComment,
        pk: int = Path(...),
        user: models.User = Depends(get_superuser)
):
    """ Create comment router
    """
    return await service.comment_s.create(schema, user_id=user.id, review_id=pk)


@comment_router.get('/{pk}', response_model=List[schemas.CommentBaseOut])
async def get_list_comment(
        pk: int = Path(...),
        user: models.User = Depends(get_user)
):
    """ Get list comments by review's pk
    """
    return await service.comment_s.filter(review_id=pk)
