import joblib
import os
from firebase_admin import storage
from threading import Lock


class ModelLoaderSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, model_path=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if model_path is None:
                        raise ValueError("Model path is required on first load")
                    print("Loading model ...")
                    cls._instance = super().__new__(cls)
                    cls._instance._load(model_path)
        return cls._instance

    def _load(self, model_path):
        bucket = storage.bucket()

        file_name_model = os.path.basename(model_path)
        blob_model = bucket.blob(f"models/{file_name_model}")

        if blob_model.exists():
            blob_model.download_to_filename(model_path)
        else:
            raise FileNotFoundError("Model not found in Firebase.")

        # Load vào RAM
        self.model = joblib.load(model_path)

    def get_model(self):
        return self.model
