from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Response model for the login endpoint, containing the JWT token for successful authentication.
    """

    jwt_token: str
    expires_in: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "a_very_secret_key_please_change"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str) -> Optional[prisma.models.User]:
    """Retrieve a user by email."""
    return await prisma.models.User.prisma().find_unique(where={"email": email})


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT access token with the provided data and expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login(email: str, password: str) -> LoginResponse:
    """
    Endpoint for user login, returning a JWT token upon successful authentication.

    Args:
    email (str): The email address of the user attempting to log in.
    password (str): The password associated with the user's email address.

    Returns:
    LoginResponse: Response model for the login endpoint, containing the JWT token for successful authentication.
    """
    user = await get_user(email)
    if not user or not verify_password(password, user.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponse(
        jwt_token=access_token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
