# thirdparty
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

# project
from src.config import settings

DEVICE_KEY_HEADER = APIKeyHeader(name="Device-UUID", auto_error=False)
CLIENT_KEY_HEADER = APIKeyHeader(name="Client-Key", auto_error=False)


def device_key_auth(device_api_key: str = Depends(DEVICE_KEY_HEADER)):
    if device_api_key != settings.DEVICE_UUID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )


def client_key_auth(client_api_key: str = Depends(CLIENT_KEY_HEADER)):
    if client_api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
