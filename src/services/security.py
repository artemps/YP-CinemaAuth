import time
import calendar
from uuid import UUID

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core import settings

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from async_fastapi_jwt_auth import AuthJWT

from repository.redis import RedisService, get_redis_service


class SecurityService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    auth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


    __slots__ = ("_secret_key", "_encryption_algorithm", "_access_token_ttl", "_refresh_token_ttl")

    def __init__(
        self,
        encryption_algorithm: str,
        access_token_ttl: int,
        refresh_token_ttl: int
    ) -> None:
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

    async def create_access_token(self, user_login: str, Authorize) -> str:
        access_token = await Authorize.create_access_token(
            subject=user_login,
            expires_time=self._refresh_token_ttl,
            algorithm=self._encryption_algorithm
        )
        return access_token

    async def create_refresh_token(self, user_login: str, Authorize) -> str:
        refresh_token = await Authorize.create_refresh_token(
            subject=user_login,
            expires_time=self._access_token_ttl,
            algorithm=self._encryption_algorithm
        )
        return refresh_token

    async def refresh_token(
            self,
            Authorize,
            redis_service: RedisService = get_redis_service()
    ):
        await Authorize.jwt_refresh_token_required()
        current_user = await Authorize.get_jwt_subject()
        new_access_token = await self.create_access_token(current_user, Authorize)
        new_refresh_token = await self.create_refresh_token(current_user, Authorize)
        jti = (await Authorize.get_raw_jwt())["jti"]

        entry = redis_service.get_token(jti)
        if entry:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token in revoke list")
        redis_service.revoke_token(jti)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    async def authenticate(
            self,
            Authorize,
            login: str,
            redis_service: RedisService = get_redis_service()
    ) -> list:
        await Authorize.jwt_required()
        current_user = await Authorize.get_jwt_subject()
        jti = (await Authorize.get_raw_jwt())["jti"]
        entry = redis_service.get_token(jti)
        if entry:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token in revoke list")
        if login != current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Have not access")

        return current_user

    async def logout(
            self,
            Authorize,
            redis_service: RedisService = get_redis_service()
    ):
        await Authorize.jwt_refresh_token_required()
        _jwt = (await Authorize.get_raw_jwt())
        exp = _jwt['exp']
        now = calendar.timegm(time.gmtime())
        redis_service.revoke_token(_jwt['jti'], exp - now)


def get_security_service() -> SecurityService:
    return SecurityService(
        encryption_algorithm=settings.encryption_algorithm,
        access_token_ttl=settings.access_token_ttl,
        refresh_token_ttl=settings.refresh_token_ttl,
    )
