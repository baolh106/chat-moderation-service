from src.shared.database.mongo.mongodb import MongoDBClient
from src.modules.key.domain.repositories import IServiceKeyRepository
from typing import Optional

class ServiceKeyRepository(IServiceKeyRepository):
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
        self.collection_name = "service_keys"

    async def find_by_key(self, api_key: str) -> Optional[dict]:
        if self.mongodb_client.db is None:
            await self.mongodb_client.connect()
        
        return await self.mongodb_client.db[self.collection_name].find_one(
            {"key": api_key, "is_active": True}
        )