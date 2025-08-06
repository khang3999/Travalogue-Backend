import os
from typing import List
from dotenv import load_dotenv
from app.repositories import tour_repository
from app.models.model_loader import ModelLoaderSingleton
from app.utils.tour_utils import extract_tour_data, calculate_related_tours


load_dotenv()

model_path = os.getenv("FILE_MODEL_PATH")
scaler_path = os.getenv("FILE_SCALER_PATH")


def get_all_tours():
    return tour_repository.get_all_tours()


def get_related_tours(behavior_locations: List[str]):
    # Tạo danh features từ danh sách tour
    list_tours = tour_repository.get_all_tours()
    list_extracted = extract_tour_data(list_tours)

    # Load model and scaler
    loader = ModelLoaderSingleton(model_path, scaler_path)
    model, scaler = loader.get_model_and_scaler()

    #  Tính toán và sắp xếp các id tour theo thứ tự liên quan
    ids_sorted = calculate_related_tours(list_extracted, behavior_locations, model, scaler)
    
    # 
    return ids_sorted



