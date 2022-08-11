from tortoise import fields, models


class Verification(models.Model):
    """ Model for confirming user registration
    """
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='verification')
