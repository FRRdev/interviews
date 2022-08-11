from typing import Optional

from fastapi import HTTPException
from tortoise.expressions import Q
from tortoise.functions import Count

from . import schemas, models
from ..base.base_service import BaseService
from .models import WorkFormat


class VacancyService(BaseService):
    model = models.Vacancy
    create_schema = schemas.CreateVacancy
    get_schema = schemas.GetVacancy

    async def create_update_vacancy_with_skills(
            self, schema, skills, update: bool = False, **kwargs
    ) -> Optional[schemas.GetVacancy]:
        """ Create/update vacancy with skills """
        self.__check_correct_work_format(schema)
        _skills = await models.Skill.filter(id__in=skills)
        if update:
            await self.update(schema, **kwargs)
            obj = await self.get_obj(**kwargs)
            await obj.skill.clear()
        else:
            obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.skill.add(*_skills)
        return await self.get(id=obj.id)

    @staticmethod
    def __check_correct_work_format(schema: schemas.CreateVacancy) -> None:
        value = schema.dict().get('work_format')
        if value and value not in [e.value for e in WorkFormat]:
            raise HTTPException(status_code=404, detail='Incorrect data for work format')

    async def list_vacancies_by_info(self, info: str, ordered: str) -> Optional[schemas.GetVacancy]:
        queryset = self.model.all()
        if info:
            queryset = queryset.filter(Q(title__icontains=info) | Q(description__icontains=info))
        if ordered:
            if ordered == 'comments':
                queryset = queryset.annotate(new_f=Count('reviews')).order_by('-new_f')
        return await queryset


class SkillService(BaseService):
    model = models.Skill
    create_schema = schemas.CreateSkill
    get_schema = schemas.GetSkill


vacancy_s = VacancyService()
skill_s = SkillService()
