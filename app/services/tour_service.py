from typing import List
from app.repositories.tour_repository import TourRepository
from app.models.model_loader import ModelLoaderSingleton
from app.utils.tour_utils import (
    create_feature,
)

tour_repository = TourRepository()


def get_all_tours():
    return tour_repository.get_all()


def get_related_tours(behaviors: List[str]):
    # Tạo danh features từ danh sách tour
    all_tours_json = tour_repository.get_all()
    all_tours_array = list(all_tours_json.values())

    # Tạo tập dữ liệu features (X) cho mô hình dự đoán là mảng 2d
    features_list = []
    for tour in all_tours_array:
        feature = create_feature(tour, behaviors)
        features_list.append(feature)

    model_loader = ModelLoaderSingleton()
    model = model_loader.get_model()
    
    probs = model.predict_proba(features_list)
    # print(probs)
    fit_probs = [prob[1] for prob in probs]
    
    # Ghép lại thành list các cặp (xác suất, tour)
    paired = list(zip(fit_probs, all_tours_array))
    
    # Sắp xếp theo xác suất giảm dần
    paired_sorted = sorted(paired, key=lambda x: x[0], reverse=True)
    sorted_tours = [p[1] for p in paired_sorted]

    return sorted_tours


# def calculate_related_score(tour_id, behavior_locations: List[str]) -> float:
#     tour = tour_repository.get_tour_by_id(tour_id)
#     if tour is None:
#         raise HTTPException(status_code=404, detail="Tour not found")
#     extracted_data = extract_tour_data(tour)
#     loader = ModelLoaderSingleton(model_path, scaler_path)
#     model, scaler = loader.get_model_and_scaler()
#     return {
#         "id": tour_id,
#         "locations": extracted_data.locations,
#         "behavior_locations": behavior_locations,
#         "rating": extracted_data.rating,
#         "related_score": predict_score(
#             extracted_data, behavior_locations, model, scaler
#         ),
#     }


# def sort_list_tours_by_score(behavior_locations: List[str]):
#     list_tours = tour_repository.get_all_tours()
#     list_extracted = extract_list_tour_data(list(list_tours.values()))

#     loader = ModelLoaderSingleton(model_path, scaler_path)
#     model, scaler = loader.get_model_and_scaler()
#     list_result = calculate_related_tours_1(
#         list_extracted, behavior_locations, model, scaler
#     )
#     return list_result
