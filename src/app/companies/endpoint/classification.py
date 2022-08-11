from typing import List
from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser, get_user
from .. import schemas, models, service

classification_router = APIRouter()


@classification_router.post('/', response_model=schemas.GetClassification)
async def create_classification(
        schema: schemas.CreateClassification,
        user: models.User = Depends(get_superuser)
):
    """ Create classification router
    """
    return await service.classification_s.create(schema)


@classification_router.get('/', response_model=List[schemas.GetClassification])
async def get_list_classification(user: models.User = Depends(get_user)):
    """ Get list of classification router
    """
    return await service.classification_s.filter(parent_id__isnull=True)


@classification_router.delete('/{pk}', status_code=204)
async def delete_classification(pk: int, user: models.User = Depends(get_superuser)):
    """ Delete classification
    """
    return await service.classification_s.delete(id=pk)
