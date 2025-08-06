from typing import List
from firebase_admin import db as firebase_db
from firebase_admin import storage
import os


# def get_cities_data():
#     cities_ref = firebase_db.reference("cities/avietnam/")
#     data = cities_ref.get()
#     all_id_cities = []
#     if not data:
#         print("No data found in cities/avietnam/")
#         return all_id_cities
#     for region_id, citiesObject in data.items():
#         for city_id, city_data in citiesObject.items():
#             all_id_cities.append(city_id)
#     return all_id_cities


def get_all_tours():
    tour_ref = firebase_db.reference("tours/")
    data = tour_ref.get()
    # list_tours = []
    if not data:
        print("No data found in tours/")
        # Xu lí json fail ở day
        return {}
    # print(List(data))
    # list_tours = List(data.values())
    return data


def get_new_data_to_training_tour():
    tour_ref = firebase_db.reference("tours/")
    data = tour_ref.get()
    all_tours = []
    if not data:
        print("No data found in tours/")
        return all_tours
    for tour_data in data.values():
        city_ids = []
        locations = tour_data.get("locations", [])
        for country in locations.values():
            city_ids.extend(country.keys())

        rating_summary = tour_data.get("ratingSummary", {})
        total = rating_summary.get("totalRatingValue", 0)
        count = rating_summary.get("totalRatingCounter", 0)
        avg_rating = total / count if count > 0 else 0

        all_tours.append(
            {
                "id": tour_data.get("id"),
                "locations": city_ids,
                "rating": avg_rating,
            }
        )
    return all_tours


def get_model_and_scaler(file_path_model, file_path_scaler):
    bucket = storage.bucket()

    file_name_model = os.path.basename(file_path_model)
    file_name_scaler = os.path.basename(file_path_scaler)
    blob_model = bucket.blob(f"models/{file_name_model}")
    blob_scaler = bucket.blob(f"models/{file_name_scaler}")

    if blob_model.exists() and blob_scaler.exists():
        blob_model.download_to_filename(file_path_model)
        blob_scaler.download_to_filename(file_path_scaler)
        return True
    return False
