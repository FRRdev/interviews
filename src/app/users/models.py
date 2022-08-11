from tortoise import fields, models, Tortoise


class User(models.Model):
    """ Model user
    """
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100, null=True)
    date_join = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_company = fields.BooleanField(default=False)
    avatar = fields.CharField(max_length=1024, null=True)

    class PydanticMeta:
        backward_relations = False
        exclude = [
            "password", "date_join", "last_login", "is_staff"
        ]


Tortoise.init_models(["src.app.users.models"], "models")
