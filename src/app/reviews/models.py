from tortoise import models, fields, Tortoise
from tortoise.validators import MinValueValidator, MaxValueValidator

from src.app.vacancies.models import Vacancy
from src.app.users.models import User


class Review(models.Model):
    """ Model of review for interview
    """
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', related_name='reviews'
    )
    advantages = fields.CharField(max_length=1000, null=True)
    disadvantages = fields.CharField(max_length=1000, null=True)
    value = fields.IntField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = fields.DatetimeField(auto_now_add=True)
    vacancy: fields.ForeignKeyRelation[Vacancy] = fields.ForeignKeyField(
        'models.Vacancy', related_name='reviews'
    )

    class PydanticMeta:
        backward_relations = True


class CommentReview(models.Model):
    """ Model of review's comment
    """
    user = fields.ForeignKeyField('models.User', related_name='comments')
    review = fields.ForeignKeyField('models.Review', related_name='comments')
    message = fields.CharField(max_length=1000)
    created_at = fields.DatetimeField(auto_now_add=True)


Tortoise.init_models(["src.app.companies.models", "src.app.vacancies.models", "src.app.reviews.models"], "models")
