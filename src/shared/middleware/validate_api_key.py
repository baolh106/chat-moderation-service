import logging
from fastapi import Depends, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from src.modules.key.domain.repositories import IServiceKeyRepository
from src.modules.key.infrastructure.mongo.service_key_repository import ServiceKeyRepository
from src.modules.key.use_case.verify_api_key import VerifyApiKeyUseCase
from src.shared.database.mongo.mongodb import mongodb_client

logger = logging.getLogger("uvicorn.error")

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_verify_api_key_use_case() -> VerifyApiKeyUseCase:
    _api_key_repo = ServiceKeyRepository(mongodb_client)
    return VerifyApiKeyUseCase(_api_key_repo)


async def validate_api_key(
    api_key: str = Security(api_key_header),
    use_case: VerifyApiKeyUseCase = Depends(get_verify_api_key_use_case)
):
    """
    Middleware xác thực API Key từ MongoDB collection 'service_keys'
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu API Key! Vui lòng cung cấp x-api-key trong header."
        )

    key_record = await use_case.execute(api_key)

    if not key_record:
        logger.warning(f"--- [AUTH] Xác thực thất bại cho API Key: {api_key} ---")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cấm truy cập! API Key không hợp lệ hoặc đã hết hạn."
        )

    logger.info(f"--- [AUTH] API Key hợp lệ: {api_key} (Service: {key_record.get('service_name')}) ---")
    return key_record