from fastapi import APIRouter
from api.endpoints.flashcards import router as route1_router
from api.endpoints.inference import router as route2_router
from api.endpoints.upload import router as route3_router
from api.endpoints.definition import router as route4_router

api_router = APIRouter()

# Include routers from the routes directory
api_router.include_router(route1_router, prefix="/route1", tags=["Route 1"])
api_router.include_router(route2_router, prefix="/route2", tags=["Route 2"])
api_router.include_router(route3_router, prefix="/route3", tags=["Route 3"])
api_router.include_router(route4_router, prefix="/route4", tags=["Route 4"])