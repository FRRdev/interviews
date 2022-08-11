from datetime import datetime
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from . import models
from ..companies.schemas import CompanyOut

CreateSkill = pydantic_model_creator(models.Skill, exclude_readonly=True, name='create_skill')
GetSkill = pydantic_model_creator(models.Skill, exclude=('vacancies',), name='get_skill')

CreateVacancy = pydantic_model_creator(models.Vacancy, name='create_vacancy', exclude_readonly=True)
GetVacancy = pydantic_model_creator(models.Vacancy, name='get_vacancy')


class VacancyBaseOut(PydanticModel):
    """ Base vacancy scheme
    """
    id: int
    title: str
    description: str
    required_experience: int
    salary: str
    work_format: models.WorkFormat
    created_at: datetime


class VacancyOut(VacancyBaseOut):
    """ Vacancy full scheme
    """
    company: CompanyOut
    skill: List[GetSkill]


# class NewSkill(BaseModel):
#     id: int
#     text: str
#
#     class Config:
#         orm_mode = True
#
#
# class NewVacancyOut(BaseModel):
#     id: int
#     title: str
#     description: str
#     required_experience: int
#     salary: str
#     work_format: models.WorkFormat
#     created_at: datetime
#     company: CompanyOut
#     reviews: List[schemas.ReviewBaseOut] = None
#
#     # skill: List[NewSkill]
#
#     class Config:
#         orm_mode = True
