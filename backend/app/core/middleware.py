from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred"}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

async def verify_api_key(request: Request):
    """Verify API key and check rate limits."""
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    
    # Find matching API key
    api_key_obj = None
    for key_obj in settings.API_KEYS.values():
        if key_obj.key == api_key:
            api_key_obj = key_obj
            break
    
    if not api_key_obj:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    if not api_key_obj.is_valid():
        raise HTTPException(
            status_code=401,
            detail="API key has expired"
        )
    
    if not api_key_obj.can_make_request():
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    
    return True 