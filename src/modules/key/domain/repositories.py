from abc import ABC, abstractmethod
from typing import Optional
from src.modules.key.domain.entities import ServiceKey

class IServiceKeyRepository(ABC):
    @abstractmethod
    async def find_by_key(self, api_key: str) -> Optional[dict]:
        pass