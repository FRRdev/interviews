from . import schemas, models
from ..base.base_service import BaseService


class ReviewService(BaseService):
    model = models.Review
    create_schema = schemas.CreateReview
    get_schema = schemas.GetReview


class CommentService(BaseService):
    model = models.CommentReview
    create_schema = schemas.CreateComment
    get_schema = schemas.GetComment


review_s = ReviewService()
comment_s = CommentService()
