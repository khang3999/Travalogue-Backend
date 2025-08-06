from fastapi import FastAPI
from app.database.firebase_config import init_firebase
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tour, test

app = FastAPI(
    title="Tour API with Firebase",
    version="1.0.0",
    description="API cho hệ thống tour du lịch sử dụng Firebase Realtime Database"
)

firebase_db = init_firebase()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc thay bằng domain cụ thể như "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(test.router)
app.include_router(tour.router)