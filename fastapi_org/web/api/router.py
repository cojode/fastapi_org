from fastapi.routing import APIRouter

from fastapi_org.web.api import building, organization

api_router = APIRouter()
api_router.include_router(organization.router, prefix="/org")
api_router.include_router(building.router, prefix="/building")
