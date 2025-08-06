import joblib
import os
from firebase_admin import storage
from threading import Lock


class ModelLoaderSingleton:
    _instance = None
    _lock = Lock()
    
    def __new__(cls, model_path, scaler_path):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("Loading model and scaler...")
                    cls._instance = super().__new__(cls)
                    cls._instance._load(model_path, scaler_path)
        return cls._instance

    def _load(self, model_path, scaler_path):
        bucket = storage.bucket()

        file_name_model = os.path.basename(model_path)
        file_name_scaler = os.path.basename(scaler_path)
        blob_model = bucket.blob(f"models/{file_name_model}")
        blob_scaler = bucket.blob(f"models/{file_name_scaler}")

        if blob_model.exists() and blob_scaler.exists():
            blob_model.download_to_filename(model_path)
            blob_scaler.download_to_filename(scaler_path)
        else:
            raise FileNotFoundError("Model or scaler not found in Firebase.")

        # Load vào RAM
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def get_model_and_scaler(self):
        return self.model, self.scaler