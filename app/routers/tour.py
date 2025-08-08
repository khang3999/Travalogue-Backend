from fastapi import APIRouter, Query

from app.services import tour_service
from app.schemas.sc_tour import BehaviorLocations
# from typing import List


router = APIRouter(prefix="/tours", tags=["tours"])


@router.get("/")
async def get_all_tours():
    return tour_service.get_all_tours()


# Khi gởi qua body phải đặt tên biết giống với trong schema BehaviorLocations
@router.post("/related")
async def get_related_tours(data: BehaviorLocations):
    return tour_service.get_related_tours(data.locations)


@router.get("/related1")
async def get_sorted_tours(behaviors: str = Query(...)):
    location_ids = behaviors.split(",") if behaviors else []
    return tour_service.get_related_tours(location_ids)


# TEST
@router.get("/scores/")
def get_tour_by_id(tour_id: str = Query(...), behavior_locations: str = Query(...)):
    location_ids = behavior_locations.split(",") if behavior_locations else []
    return tour_service.calculate_related_score(tour_id, location_ids)


# TEST
@router.get("/sort/")
def sort_list_tours(tour_id: str = Query(...), behavior_locations: str = Query(...)):
    location_ids = behavior_locations.split(",") if behavior_locations else []
    return tour_service.sort_list_tours_by_score(location_ids)
