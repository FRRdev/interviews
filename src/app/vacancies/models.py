from enum import Enum
from tortoise import models, fields, Tortoise

from src.app.companies.models import Company


class WorkFormat(str, Enum):
    REMOTE = 'remote'
    OFFICE = 'office'
    PART_TIME = 'part-time'


class Skill(models.Model):
    """ Model of skill for vacancy
    """
    text = fields.CharField(max_length=150)

    vacancies: fields.ManyToManyRelation['Vacancy']

    class PydanticMeta:
        backward_relations = True


class Vacancy(models.Model):
    """ Model of company's vacancy
    """
    title = fields.CharField(max_length=150)
    description = fields.TextField()
    required_experience = fields.SmallIntField()
    salary = fields.IntField()
    work_format = fields.CharEnumField(WorkFormat, default=WorkFormat.OFFICE)
    created_at = fields.DatetimeField(auto_now_add=True)
    company: fields.ForeignKeyRelation[Company] = fields.ForeignKeyField(
        'models.Company', related_name='vacancies'
    )
    skill: fields.ManyToManyRelation[Skill] = fields.ManyToManyField(
        'models.Skill', related_name='vacancies', through='vacancy_skill'
    )

    class PydanticMeta:
        backward_relations = True

    class Meta:
        indexes = ("title", "description")
        ordering = ("-created_at",)


Tortoise.init_models(["src.app.reviews.models", "src.app.companies.models", "src.app.vacancies.models"], "models")
