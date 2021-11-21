from fastapi import FastAPI
from app.api.v1_endpoints.index import router as api_router
from app.core.conf import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Fast API service for lishe bora shipping service",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.include_router(router=api_router, prefix=settings.API_V1_STR)
