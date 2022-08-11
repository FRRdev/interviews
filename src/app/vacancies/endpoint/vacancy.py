from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params, paginate, Page

from src.app.auth.permissions import get_company, get_user, get_author_user
from src.app.users.models import User
from .. import schemas, service

vacancy_router = APIRouter()


@vacancy_router.post('/', response_model=schemas.VacancyOut)
async def create_vacancy(
        vacancy: schemas.CreateVacancy,
        skills: List[int],
        user: User = Depends(get_company)
):
    """ Create vacancy router
    """
    return await service.vacancy_s.create_update_vacancy_with_skills(vacancy, skills)


@vacancy_router.get('/', response_model=Page[schemas.VacancyBaseOut])
async def search_vacancies(
        params: Params,
        info: str = Query(None),
        ordered: str = Query(None, enum=["comments", ]),
        user: User = Depends(get_user)):
    """ Search vacancy by some field
    """
    queryset = await service.vacancy_s.list_vacancies_by_info(info, ordered)
    return paginate(queryset, params)


@vacancy_router.get('/{pk}', response_model=schemas.GetVacancy)
async def get_single_vacancy(pk: int, user: User = Depends(get_user)):
    """ Get single vacancy router
    """
    return await service.vacancy_s.get(pk=pk)


@vacancy_router.put('/{pk}', response_model=schemas.VacancyOut)
async def update_vacancy(
        pk: int,
        vacancy: schemas.CreateVacancy,
        skills: List[int],
        user: User = Depends(get_author_user)
):
    """ Create vacancy router
    """
    return await service.vacancy_s.create_update_vacancy_with_skills(
        vacancy, skills, update=True, pk=pk
    )


@vacancy_router.delete('/{pk}', status_code=204)
async def delete_vacancy(pk: int, user: User = Depends(get_author_user)):
    """ Delete vacancy by id
    """
    return await service.vacancy_s.delete(id=pk)
