from typing import List
from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, paginate, Params

from .. import schemas, models, service
from src.app.auth.permissions import get_company, get_user, get_author_user

company_router = APIRouter()


@company_router.post('/', response_model=schemas.GetCompany)
async def create_company(
        company: schemas.CreateCompany,
        addresses: List[schemas.CreateAddress],
        user: models.User = Depends(get_company)
):
    """ Create company router
    """
    return await service.company_s.create_company_with_address(company, addresses, owner_id=user.id)


@company_router.get('/', response_model=Page[schemas.CompanyFullOut])
async def get_list_company(
        params: Params,
        user: models.User = Depends(get_user)
):
    """ Create company router
    """
    queryset = await service.company_s.all()
    return paginate(queryset, params)


@company_router.get('/{pk}', response_model=schemas.GetCompany)
async def get_single_company(
        pk: int = Path(...),
        user: models.User = Depends(get_user)
):
    """ get singe company by pk
    """
    return await service.company_s.get(pk=pk)


@company_router.put('/{pk}', response_model=schemas.GetCompany)
async def update_company(
        company: schemas.CreateCompany,
        pk: int = Path(...),
        user: models.User = Depends(get_author_user)
):
    """ get singe company by pk
    """
    return await service.company_s.update(schema=company, pk=pk)


@company_router.delete('/{pk}', status_code=204)
async def delete_company(pk: int, user: models.User = Depends(get_author_user)):
    """ Delete company
    """
    return await service.company_s.delete(id=pk)
