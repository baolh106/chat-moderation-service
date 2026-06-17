import logging
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handles FastAPI's HTTPException (ví dụ: 401, 403, 404), trả về JSON response chuẩn hóa.
    """
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail} "
        f"for path {request.url.path} from {request.client.host}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles FastAPI's RequestValidationError (lỗi validate Pydantic cho request body/query params).
    """
    errors = []
    for error in exc.errors():
        # Lấy đường dẫn đến trường bị lỗi (ví dụ: body.image_url)
        loc = ".".join(map(str, error["loc"]))
        errors.append(f"{loc}: {error['msg']}")
    
    error_message = "Dữ liệu đầu vào không hợp lệ"
    if errors:
        error_message = f"Lỗi xác thực: {'; '.join(errors)}"

    logger.warning(
        f"Request Validation Error for path {request.url.path} from {request.client.host}: {error_message}"
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "message": error_message, "details": exc.errors()},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles tất cả các lỗi không được xử lý khác, trả về lỗi 500 Internal Server Error.
    """
    logger.exception(f"Unhandled Exception for path {request.url.path} from {request.client.host}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Lỗi máy chủ nội bộ"},
    )

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)