from typing import List
from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_user, get_author_user
from .. import schemas, models, service

address_router = APIRouter()


@address_router.post('/add/{pk}', response_model=schemas.GetAddress)
async def add_address(
        pk: int,
        schema: schemas.CreateAddress,
        user: models.User = Depends(get_author_user)
):
    """ Create address router
    """
    return await service.address_s.create(schema, company_id=pk)


@address_router.get('/{pk}', response_model=List[schemas.AddressBaseOut])
async def get_list_addresses(pk: int, user: models.User = Depends(get_user)):
    """ Get list of classification router
    """
    return await service.address_s.filter(company_id=pk)


@address_router.delete('/{pk}', status_code=204)
async def delete_address(pk: int, user: models.User = Depends(get_author_user)):
    """ Delete address
    """
    return await service.address_s.delete(id=pk)
