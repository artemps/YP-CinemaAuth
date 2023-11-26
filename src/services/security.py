import time
from uuid import UUID

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core import settings


class SecurityService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    auth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    __slots__ = ("_secret_key", "_encryption_algorithm", "_access_token_ttl", "_refresh_token_ttl")

    def __init__(
        self,
        secret_key: str,
        encryption_algorithm: str,
        access_token_ttl: int,
        refresh_token_ttl: int,
    ) -> None:
        self._secret_key = secret_key
        self._encryption_algorithm = encryption_algorithm
        self._access_token_ttl = access_token_ttl
        self._refresh_token_ttl = refresh_token_ttl

    def verify_password(self, plain_password: str, hashed_password: str, raise_exception: bool = True) -> bool:
        is_verified = self.pwd_context.verify(plain_password, hashed_password)
        if not is_verified and raise_exception:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        return is_verified

    def create_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, user_id: UUID) -> str:
        payload = {"user_id": str(user_id), "expires": time.time() + self._refresh_token_ttl}
        token = jwt.encode(payload, key=self._secret_key, algorithm=self._encryption_algorithm)
        return token

    def authenticate(self, token: str) -> UUID:
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required")

        try:
            payload = jwt.decode(token, key=self._secret_key, algorithms=[self._encryption_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")

        expire = payload.get("expires")

        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")

        if time.time() > expire:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        return UUID(payload["user_id"])


def get_security_service() -> SecurityService:
    return SecurityService(
        secret_key=settings.secret_key,
        encryption_algorithm=settings.encryption_algorithm,
        access_token_ttl=settings.access_token_ttl,
        refresh_token_ttl=settings.refresh_token_ttl,
    )
