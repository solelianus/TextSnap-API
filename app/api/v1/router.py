from fastapi import APIRouter
from app.api.v1.endpoints import generate, fonts, admin

api_router = APIRouter()

api_router.include_router(
    generate.router,
    prefix="/generate",
    tags=["generate"]
)

api_router.include_router(
    fonts.router,
    prefix="/fonts",
    tags=["fonts"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
) 