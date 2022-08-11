from datetime import datetime
from typing import List
from pydantic import validator
from pydantic.main import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.users.schemas import UserBase
from . import models

GetReview = pydantic_model_creator(models.Review, name='get_review')

CreateComment = pydantic_model_creator(
    models.CommentReview, exclude_readonly=True, exclude=('user_id', 'review_id'), name='create_comment'
)
GetComment = pydantic_model_creator(models.CommentReview, name='get_comment')


class CreateReview(BaseModel):
    """ Create review scheme
    """
    advantages: str
    disadvantages: str
    value: int

    @validator('value')
    def check_value(cls, v):
        if v > 10 or v < 0:
            raise ValueError('Value should be from 0 to 10')
        return v

    class Config:
        orm_mode = True


class CommentBaseOut(BaseModel):
    """ Comment scheme base
    """
    id: int
    user: UserBase
    message: str
    created_at: datetime


class ReviewBaseOut(BaseModel):
    """ Review scheme base
    """
    id: int
    user: UserBase
    advantages: str
    disadvantages: str
    value: int
    comments: List[CommentBaseOut] = None
