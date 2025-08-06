from typing import List, Dict
from sklearn.base import BaseEstimator, TransformerMixin
from app.schemas.sc_tour import TourDataExtracted
from app.utils.location_utils import extract_city_ids
from app.utils.rating_utils import avg_rating


# Tính toán điểm số dự đoán cho từng tour - đưa qua backend
# Dựa trên số lượng địa điểm giao nhau và rating đã nội suy
def predict_score(
    data_tour_extracted: TourDataExtracted,
    user_locations: List[str],
    model: BaseEstimator,
    scaler: TransformerMixin,
):
    # Đếm tỉnh trùng
    overlap_count = len(set(data_tour_extracted.locations) & set(user_locations))
    # Tính delta - độ lệch giữa số lượng địa điểm giao nhau và tổng số địa điểm
    max_len = max(len(data_tour_extracted.locations), len(user_locations))
    delta = 1 - (overlap_count / max_len) if max_len > 0 else 1
    # Chuyển đổi rating về dạng đã nội suy
    rating_scaled = scaler.transform([[data_tour_extracted.rating]])[0][0]
    # Tạo đặc trưng (X) của từng tour để mô hình dự đoán
    features = [[overlap_count, delta, rating_scaled]]
    return model.predict_proba(features)[0][1]


# Hàm tính toán và sắp xếp bằng Machine Learning
def calculate_related_tours(
    list_data_tour_extracted: List[TourDataExtracted],
    behavior_locations: List[str],
    model: BaseEstimator,
    scaler: TransformerMixin,
) -> List[str]:
    # Sắp xếp tour theo độ phù hợp giảm dần trả về mảng ids tour đã sắp xếp
    sorted_tours = sorted(
        list_data_tour_extracted,
        key=lambda data_tour: predict_score(
            data_tour, behavior_locations, model, scaler
        ),
        reverse=True,
    )
    return [tour.id for tour in sorted_tours]


# Hàm tính toán và sắp xếp bằng Machine Learning
def calculate_related_tours_1(
    list_data_tour_extracted: List[TourDataExtracted],
    behavior_locations: List[str],
    model: BaseEstimator,
    scaler: TransformerMixin,
) -> Dict[str, float]:
    # Tính score cho từng tour
    id_score_map = {
        tour.id: predict_score(tour, behavior_locations, model, scaler)
        for tour in list_data_tour_extracted
    }
    # Sắp xếp tour theo độ phù hợp giảm dần
    sorted_tours = dict(
        sorted(id_score_map.items(), key=lambda item: item[1], reverse=True)
    )
    return sorted_tours


# Hàm chuyển đổi dữ liệu từ Firebase để training mô hình
def extract_list_tour_data(list_tours) -> List[TourDataExtracted]:
    list_features = []
    for tour in list_tours:
        temp = extract_tour_data(tour)
        list_features.append(temp)
    return list_features


def extract_tour_data(tour_data) -> TourDataExtracted:
    # Process locations
    locations = tour_data.get("locations", {})
    city_ids = extract_city_ids(locations)
    # Process rating
    rating_summary = tour_data.get("ratingSummary", {})
    average_rating = avg_rating(rating_summary)

    feature = TourDataExtracted(
        id=tour_data.get("id"),
        locations=city_ids,
        rating=average_rating,
    )
    # list_features.append(feature)
    return feature
