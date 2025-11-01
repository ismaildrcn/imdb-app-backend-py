import jwt

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import settings

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,
            detail="Invalid token",
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return payload

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": int(expire.timestamp())})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token