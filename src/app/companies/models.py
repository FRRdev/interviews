from tortoise import fields, models, Tortoise

from src.app.users.models import User


class Classification(models.Model):
    """Category for company
    """
    name = fields.CharField(max_length=150)
    parent: fields.ForeignKeyNullableRelation['Classification'] = fields.ForeignKeyField(
        'models.Classification', related_name='children', null=True
    )
    children: fields.ReverseRelation['Classification']
    companies: fields.ReverseRelation['Company']

    class PydanticMeta:
        backward_relations = True
        exclude = ["companies", "parent"]
        allow_cycles = True
        max_recursion = 4


class Address(models.Model):
    """Address of a company
    """
    country = fields.CharField(max_length=150)
    city = fields.CharField(max_length=150)
    street = fields.CharField(max_length=150, null=True)
    house = fields.CharField(max_length=150, null=True)
    company: fields.ForeignKeyRelation['Company'] = fields.ForeignKeyField(
        'models.Company', related_name='addresses'
    )


class Company(models.Model):
    """ Model of Company
    """
    name = fields.CharField(max_length=150)
    created_at = fields.DatetimeField(auto_now_add=True)
    classification: fields.ForeignKeyRelation[Classification] = fields.ForeignKeyField(
        'models.Classification', related_name='companies', null=True
    )
    owner: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', related_name='companies'
    )

    addresses: fields.ReverseRelation['Address']
    workers: fields.ReverseRelation[User]

    class PydanticMeta:
        backward_relations = True

    class Meta:
        ordering = ("-created_at",)


Tortoise.init_models(["src.app.vacancies.models", "src.app.companies.models"], "models")
