from typing import List
from fastapi import APIRouter, Depends, Path

from .. import schemas, models, service
from src.app.auth.permissions import get_user

review_router = APIRouter()


@review_router.post('/{pk}', response_model=schemas.ReviewBaseOut)
async def create_review(
        company: schemas.CreateReview,
        pk: int = Path(...),
        user: models.User = Depends(get_user)
):
    """ Create company router
    """
    return await service.review_s.create(company, user_id=user.id, vacancy_id=pk)


@review_router.get('/{pk}', response_model=List[schemas.ReviewBaseOut])
async def get_list_review(
        pk: int = Path(...),
        user: models.User = Depends(get_user)
):
    """ Get list reviews router
    """
    return await service.review_s.filter(vacancy_id=pk)
