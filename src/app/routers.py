from fastapi import APIRouter
from src.app.auth.api import auth_router
from src.app.users.endpoint import users, admin
from src.app.companies.endpoint import classification, company, address
from src.app.vacancies.endpoint import skill, vacancy
from src.app.reviews.endpoint import review, comment

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=["login"])
api_router.include_router(users.user_router, prefix='/user', tags=["user"])
api_router.include_router(admin.admin_router, prefix='/admin/user', tags=["admin"])
api_router.include_router(classification.classification_router, prefix='/classification', tags=["classification"])
api_router.include_router(company.company_router, prefix='/company', tags=["company"])
api_router.include_router(address.address_router, prefix='/address', tags=["address"])
api_router.include_router(skill.skill_router, prefix='/skill', tags=["skill"])
api_router.include_router(vacancy.vacancy_router, prefix='/vacancy', tags=["vacancy"])
api_router.include_router(review.review_router, prefix='/review', tags=["review"])
api_router.include_router(comment.comment_router, prefix='/comment', tags=["comment"])
