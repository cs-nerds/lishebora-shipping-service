from fastapi.routing import APIRouter

from app.api.v1_endpoints.country import router as country_api_router
from app.api.v1_endpoints.location import router as location_api_router
from app.api.v1_endpoints.shipment import router as shipment_api_router

router = APIRouter()

router.include_router(
    router=country_api_router, prefix="/countries", tags=["countries"]
)
router.include_router(
    router=location_api_router, prefix="/locations", tags=["locations"]
)
router.include_router(
    router=shipment_api_router, prefix="/shipments", tags=["shipments"]
)
