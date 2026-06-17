import os
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from src.config.database.mongodb import mongo_config

logger = logging.getLogger("uvicorn.error")

class MongoDBClient:
    def __init__(self):
        self.uri = mongo_config.connection_uri
        self.db_name = mongo_config.db_name
        self.max_retries = int(os.getenv("MONGO_MAX_RETRIES", "5"))
        self.retry_delay = int(os.getenv("MONGO_RETRY_DELAY", "2000")) / 1000.0 # Chuyển ms sang s
        self.client = None
        self.db = None

    async def connect(self):
        attempt = 0
        while attempt < self.max_retries:
            try:
                logger.info(f"Đang kết nối tới MongoDB (Lần thử {attempt + 1}/{self.max_retries})...")
                self.client = AsyncIOMotorClient(
                    self.uri,
                    server_api=ServerApi('1'),
                    serverSelectionTimeoutMS=30000,
                    connectTimeoutMS=30000
                )
                # Kiểm tra kết nối bằng lệnh ping
                await self.client.admin.command('ping')
                self.db = self.client[self.db_name]
                logger.info(f"Kết nối MongoDB thành công!")
                return
            except ConnectionFailure as e:
                attempt += 1
                logger.error(f"Kết nối thất bại: {e}")
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.critical("Không thể kết nối tới MongoDB sau 3 lần thử.")
                    raise e

    def close(self):
        if self.client:
            self.client.close()

# Khởi tạo singleton instance để dùng chung
mongodb_client = MongoDBClient()