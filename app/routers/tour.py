from fastapi import APIRouter

from app.services import tour_service
from app.schemas.sc_tour import BehaviorLocations

router = APIRouter(prefix="/tours", tags=["tours"])


@router.get("/")
async def get_all_tours():
    return tour_service.get_all_tours()


@router.post("/related")
async def get_related_tours(filter: BehaviorLocations):
    return tour_service.get_related_tours(filter.locations)
