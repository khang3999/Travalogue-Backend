import os
from fastapi import FastAPI
from app.database.firebase_config import init_firebase
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tour, test
from app.models.model_loader import ModelLoaderSingleton

from dotenv import load_dotenv


class MainApp:
    def __init__(self):
        load_dotenv()
        model_path = os.getenv("FILE_MODEL_PATH")

        # Khởi tạo firebase
        init_firebase()

        # Load model
        self.model_loader  = ModelLoaderSingleton(model_path)
        model = self.model_loader.get_model().__class__
        print(model,'ss')

        self.app = FastAPI(
            title="Tour API with Firebase",
            version="1.0.0",
            description="API cho hệ thống tour du lịch sử dụng Firebase Realtime Database",
        )

        self._configure_middlewares()
        self._include_routes()

    def _configure_middlewares(self):
        # Cấu hình CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # hoặc domain cụ thể
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )


    def _include_routes(self):
        self.app.add_api_route("/", lambda: {"message": "hello world"})
        self.app.include_router(test.router)
        self.app.include_router(tour.router)
        
        
main_app = MainApp() # Gọi __new__ -> __init__

# Gán lại app trong main_app = app để có thể xài ở nơi khác chỉ cần import
app = main_app.app