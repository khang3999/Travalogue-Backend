from firebase_admin import db
# import os
class TourRepository:
    def __init__(self):
        pass


    def get_all(self):
        tour_ref = db.reference("tours/")
        data = tour_ref.get()
        if not data:
            print("No data found in tours/")
            return {}
        return data


    # def get_new_data_to_training_tour():
    #     tour_ref = db.reference("tours/")
    #     data = tour_ref.get()
    #     all_tours = []
    #     if not data:
    #         print("No data found in tours/")
    #         return all_tours
    #     for tour_data in data.values():
    #         city_ids = []
    #         locations = tour_data.get("locations", [])
    #         for country in locations.values():
    #             city_ids.extend(country.keys())

    #         rating_summary = tour_data.get("ratingSummary", {})
    #         total = rating_summary.get("totalRatingValue", 0)
    #         count = rating_summary.get("totalRatingCounter", 0)
    #         avg_rating = total / count if count > 0 else 0

    #         all_tours.append(
    #             {
    #                 "id": tour_data.get("id"),
    #                 "locations": city_ids,
    #                 "rating": avg_rating,
    #             }
    #         )
    #     return all_tours


    # def get_model_and_scaler(file_path_model, file_path_scaler):
    #     bucket = storage.bucket()

    #     file_name_model = os.path.basename(file_path_model)
    #     file_name_scaler = os.path.basename(file_path_scaler)
    #     blob_model = bucket.blob(f"models/{file_name_model}")
    #     blob_scaler = bucket.blob(f"models/{file_name_scaler}")

    #     if blob_model.exists() and blob_scaler.exists():
    #         blob_model.download_to_filename(file_path_model)
    #         blob_scaler.download_to_filename(file_path_scaler)
    #         return True
    #     return False

    # def get_tour_by_id(tour_id: str):
    #     tour_ref = db.reference(f"tours/{tour_id}")
    #     data = tour_ref.get()
    #     if not data:
    #         print(f"No data found for tour ID: {tour_id}")
    #         return None
    #     return data

