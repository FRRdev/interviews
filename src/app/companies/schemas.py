from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from datetime import datetime
from typing import List
from pydantic.main import BaseModel

from src.app.users.schemas import UserPublic
from . import models


class ClassificationBaseOut(BaseModel):
    """ Classification Base scheme
    """
    name: str


CreateClassification = pydantic_model_creator(
    models.Classification, name='create_classification', exclude_readonly=True
)
GetClassification = pydantic_model_creator(models.Classification, name='get_classification')

CreateCompany = pydantic_model_creator(
    models.Company, name='create_company', exclude=('owner_id',), exclude_readonly=True
)
GetCompany = pydantic_model_creator(models.Company, name='get_company')


class CompanyOut(BaseModel):
    """ Company base out scheme
    """
    id: int
    name: str


CreateAddress = pydantic_model_creator(
    models.Address, name='create_address', exclude=('company_id',), exclude_readonly=True
)
GetAddress = pydantic_model_creator(models.Address, name='get_address')


class AddressBaseOut(PydanticModel):
    """ Address Base scheme
    """
    id: int
    country: str
    city: str
    street: str
    house: str


class AddressOut(AddressBaseOut):
    """ Address out scheme
    """
    company: CompanyOut


# class AddressOutForCompany(PydanticModel):
#     id: int
#     country: str
#     city: str
#     street: str
#     house: str


class CompanyFullOut(PydanticModel):
    """ Company full scheme
    """
    id: int
    name: str
    created_at: datetime
    classification: ClassificationBaseOut
    owner: UserPublic
    addresses: List[AddressBaseOut]
