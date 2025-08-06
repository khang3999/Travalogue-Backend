import os
from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException
from app.repositories import tour_repository
from app.models.model_loader import ModelLoaderSingleton
from app.utils.tour_utils import (
    extract_list_tour_data,
    calculate_related_tours,
    calculate_related_tours_1,
    extract_tour_data,
    predict_score,
)


load_dotenv()

model_path = os.getenv("FILE_MODEL_PATH")
scaler_path = os.getenv("FILE_SCALER_PATH")


def get_all_tours() -> List[dict]:
    # rs = tour_repository.get_all_tours()
    return tour_repository.get_all_tours()
    # return list(rs.values()) if rs else []


def get_related_tours(behavior_locations: List[str]):
    # Tạo danh features từ danh sách tour
    list_tours = tour_repository.get_all_tours()
    list_extracted = extract_list_tour_data(list(list_tours.values()))

    # Load model and scaler
    loader = ModelLoaderSingleton(model_path, scaler_path)
    model, scaler = loader.get_model_and_scaler()

    # Tính toán và sắp xếp các id tour theo thứ tự liên quan
    ids_sorted = calculate_related_tours(
        list_extracted, behavior_locations, model, scaler
    )

    sorted_list_tours = [{**list_tours[i]} for i in ids_sorted if i in list_tours]
    return sorted_list_tours


def calculate_related_score(tour_id, behavior_locations: List[str]) -> float:
    tour = tour_repository.get_tour_by_id(tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    extracted_data = extract_tour_data(tour)
    loader = ModelLoaderSingleton(model_path, scaler_path)
    model, scaler = loader.get_model_and_scaler()
    return {
        "id": tour_id,
        "locations": extracted_data.locations,
        "behavior_locations": behavior_locations,
        "rating": extracted_data.rating,
        "related_score": predict_score(
            extracted_data, behavior_locations, model, scaler
        ),
    }


def sort_list_tours_by_score(behavior_locations: List[str]):
    list_tours = tour_repository.get_all_tours()
    list_extracted = extract_list_tour_data(list(list_tours.values()))

    loader = ModelLoaderSingleton(model_path, scaler_path)
    model, scaler = loader.get_model_and_scaler()
    list_result = calculate_related_tours_1(
        list_extracted, behavior_locations, model, scaler
    )
    return list_result
