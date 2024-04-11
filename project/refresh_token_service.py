from datetime import datetime, timedelta

import prisma
import prisma.models
from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    Response model after successfully refreshing the JWT authentication token. It includes the new JWT token.
    """

    access_token: str
    refresh_token: str


SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refreshes the JWT authentication token using a refresh token.

    Args:
        refresh_token (str): The refresh token issued to the user during the initial login or the last token refresh.

    Returns:
        RefreshTokenResponse: Response model after successfully refreshing the JWT authentication token. It includes the new JWT token.

    Raises:
        HTTPException: If the refresh token is not found or the token is expired.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    auth_token_record = await prisma.models.AuthToken.prisma().find_unique(
        where={"token": refresh_token}
    )
    if auth_token_record is None or auth_token_record.expiresAt < datetime.now():
        raise HTTPException(
            status_code=401, detail="Refresh token expired or not found"
        )
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    await prisma.models.AuthToken.prisma().update(
        where={"token": refresh_token},
        data={
            "token": new_refresh_token,
            "expiresAt": datetime.now() + timedelta(days=7),
        },
    )
    return RefreshTokenResponse(
        access_token=new_access_token, refresh_token=new_refresh_token
    )


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Creates a new JWT access token.

    Args:
        data (dict): The payload to encode in the JWT.
        expires_delta (timedelta): The expiry duration of the token.

    Returns:
        str: The JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_delta: timedelta = timedelta(days=7)
) -> str:
    """
    Creates a new JWT refresh token.

    Args:
        data (dict): The payload to include in the token, typically the user identifier.
        expires_delta (timedelta): How long until the token expires, defaults to 7 days.

    Returns:
        str: The JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
