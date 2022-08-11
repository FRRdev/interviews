from typing import Optional

from src.app.base.base_service import BaseService
from . import schemas, models


class CompanyService(BaseService):
    model = models.Company
    create_schema = schemas.CreateCompany
    get_schema = schemas.GetCompany

    async def create_company_with_address(self, schema, addresses, **kwargs) \
            -> Optional[schemas.GetCompany]:
        company_obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        for address in addresses:
            await address_s.create(address, company_id=company_obj.id)
        return await company_s.get(id=company_obj.id)


class ClassificationService(BaseService):
    model = models.Classification
    create_schema = schemas.CreateClassification
    get_schema = schemas.GetClassification


class AddressService(BaseService):
    model = models.Address
    create_schema = schemas.CreateAddress
    get_schema = schemas.GetAddress


company_s = CompanyService()
classification_s = ClassificationService()
address_s = AddressService()
