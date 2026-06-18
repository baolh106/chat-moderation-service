import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from src.shared.middleware.error_handler import register_error_handlers
from src.shared.database.mongo.mongodb import mongodb_client
from src.modules.detector.infrastructure.web.fastapi_app import router as detector_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Bootstrap: Khởi tạo kết nối DB khi app start
    await mongodb_client.connect()
    yield
    # Cleanup: Đóng kết nối khi app shut down
    mongodb_client.close()

app = FastAPI(title="AI Chat Moderation Service", lifespan=lifespan)

# Register error handlers
register_error_handlers(app)

app.include_router(detector_router)

if __name__ == "__main__":
    # Lấy cấu hình từ biến môi trường hoặc sử dụng giá trị mặc định
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    reload = os.getenv("APP_RELOAD", "True").lower() == "true"

    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=reload,
    )