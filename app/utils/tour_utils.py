from typing import List
from app.utils.location_utils import flatten_location
from app.utils.rating_utils import avg_rating


# Tính toán điểm số dự đoán cho từng tour - đưa qua backend
# Dựa trên số lượng địa điểm giao nhau và rating đã nội suy
# def predict_score(
#     data_tour_extracted: TourDataExtracted,
#     user_locations: List[str],
#     model: BaseEstimator,
#     scaler: TransformerMixin,
# ):
#     # Đếm tỉnh trùng
#     overlap_count = len(set(data_tour_extracted.locations) & set(user_locations))
#     # Tính delta - độ lệch giữa số lượng địa điểm giao nhau và tổng số địa điểm
#     max_len = max(len(data_tour_extracted.locations), len(user_locations))
#     delta = 1 - (overlap_count / max_len) if max_len > 0 else 1
#     # Chuyển đổi rating về dạng đã nội suy
#     rating_scaled = scaler.transform([[data_tour_extracted.rating]])[0][0]
#     # Tạo đặc trưng (X) của từng tour để mô hình dự đoán
#     features = [[overlap_count, delta, rating_scaled]]
#     return model.predict_proba(features)[0][1]


# Hàm tính toán và sắp xếp bằng Machine Learning
# def calculate_related_tours(
#     list_data_tour_extracted: List[TourDataExtracted],
#     behavior_locations: List[str],
#     model: BaseEstimator,
#     scaler: TransformerMixin,
# ) -> List[str]:
#     # Sắp xếp tour theo độ phù hợp giảm dần trả về mảng ids tour đã sắp xếp
#     sorted_tours = sorted(
#         list_data_tour_extracted,
#         key=lambda data_tour: predict_score(
#             data_tour, behavior_locations, model, scaler
#         ),
#         reverse=True,
#     )
#     return [tour.id for tour in sorted_tours]


# # Hàm tính toán và sắp xếp bằng Machine Learning
# def calculate_related_tours_1(
#     list_data_tour_extracted: List[TourDataExtracted],
#     behavior_locations: List[str],
#     model: BaseEstimator,
#     scaler: TransformerMixin,
# ) -> Dict[str, float]:
#     # Tính score cho từng tour
#     id_score_map = {
#         tour.id: predict_score(tour, behavior_locations, model, scaler)
#         for tour in list_data_tour_extracted
#     }
#     # Sắp xếp tour theo độ phù hợp giảm dần
#     sorted_tours = dict(
#         sorted(id_score_map.items(), key=lambda item: item[1], reverse=True)
#     )
#     return sorted_tours


# # Hàm chuyển đổi dữ liệu từ Firebase để training mô hình
# def extract_list_tour_data(list_tours, behaviors) -> List[TourDataExtracted]:
#     extracted_tour_data_list = []
#     for tour in list_tours:
#         temp = extract_tour_data(tour)
#         list_features.append(temp)
#     return extracted_tour_data_list


def create_feature(tour, behaviors: List[str]):
    # locations
    locations = tour.get("locations", {})
    flatten_locations = (
        flatten_location(locations) if isinstance(locations, dict) else []
    )

    # rating
    rating_summary = tour.get("ratingSummary", {})
    average_rating = float(avg_rating(rating_summary) or 0.0)

    # Tìm phần tử giao nhau <-> tỉnh trùng nhay
    overlap_count = len(set(flatten_locations) & set(behaviors))
    # Chọn số phần tử của behaviors hoặc flatten_locations(city ids)
    max_len = max(len(flatten_locations), len(behaviors))
    # Tính delta - độ lệch giữa số lượng địa điểm giao nhau và tổng số địa điểm
    delta = float((overlap_count / max_len) if max_len > 0 else 0.0)
    # Tính tỉ số của rating về [0, 1]
    scaled_rating = average_rating / 5.0

    feature = [overlap_count, delta, scaled_rating]
    return feature
