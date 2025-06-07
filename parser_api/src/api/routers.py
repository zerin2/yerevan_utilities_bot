from fastapi import APIRouter

from api.endpoints import parser_router

main_router = APIRouter()

main_router.include_router(
    parser_router,
    prefix='/parser',
    tags=['parser'],
)
