from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
from app.schemas.sc_tour import TourDataExtracted
from app.utils.location_utils import extract_city_ids
from app.utils.rating_utils import avg_rating


# Tính toán điểm số dự đoán cho từng tour - đưa qua backend
# Dựa trên số lượng địa điểm giao nhau và rating đã nội suy
def predict_score(
    data_tour_extracted, user_locations, model: BaseEstimator, scaler: TransformerMixin
):
    # Đếm tỉnh trùng
    overlap_count = len(set(data_tour_extracted["locations"]) & set(user_locations))
    # Tính delta - độ lệch giữa số lượng địa điểm giao nhau và tổng số địa điểm
    max_len = max(len(data_tour_extracted["locations"]), len(user_locations))
    delta = 1 - (overlap_count / max_len) if max_len > 0 else 1
    # Chuyển đổi rating về dạng đã nội suy
    rating_scaled = scaler.transform([[data_tour_extracted["rating"]]])[0][0]
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
    # for _ in list_data_tour_extracted:
    # Sắp xếp tour theo độ phù hợp giảm dần
    sorted_tours = sorted(
        list_data_tour_extracted,
        key=lambda data_tour: predict_score(
            data_tour, behavior_locations, model, scaler
        ),
        reverse=True,
    )
    return [tour["id"] for tour in sorted_tours]


# Hàm chuyển đổi dữ liệu từ Firebase để training mô hình
def extract_tour_data(list_tours) -> List[TourDataExtracted]:
    list_features = []
    for tour in list_tours:
        # Process locations
        locations = tour.get("locations", {})
        city_ids = extract_city_ids(locations)
        # Process rating
        rating_summary = tour.get("ratingSummary", {})
        average_rating = avg_rating(rating_summary)

        feature = TourDataExtracted(
            id=tour.get("id"),
            locations=city_ids,
            rating=average_rating,
        )
        list_features.append(feature)
    return list_features
