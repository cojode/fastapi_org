from fastapi.routing import APIRouter

from fastapi_org.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
