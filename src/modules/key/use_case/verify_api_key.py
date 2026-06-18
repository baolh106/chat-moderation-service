from src.modules.key.domain.repositories import IServiceKeyRepository

class VerifyApiKeyUseCase:
    def __init__(self, repository: IServiceKeyRepository):
        self.repository = repository

    async def execute(self, api_key: str):
        key_record = await self.repository.find_by_key(api_key)
        return key_record