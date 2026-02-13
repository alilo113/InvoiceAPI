# Implementing API key authentication for the API endpoints and API key validation logic.
# auth.py
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request

# Define the API key header
API_KEY_HEADER_NAME = "X-API-key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

# A simple in-memory store for valid API keys (for demonstration purposes)
VALID_API_KEYS = {
    "your-secure-api-key-1",
    "your-secure-api-key-2",
}

async def get_api_key(request: Request, api_key: str = Security(api_key_header)):
    if api_key is None: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,        
            detail= "Api key not provided"    
        )
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,        
            detail= "Invalid API key"    
        )