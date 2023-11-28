import calendar
import time

from async_fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core import settings
from repository.redis import RedisService, get_redis_service


class SecurityService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    async def create_access_token(self, user_login: str, auth: AuthJWT) -> str:
        access_token = await auth.create_access_token(
            subject=user_login,
            expires_time=self._refresh_token_ttl,
            algorithm=self._encryption_algorithm
        )
        return access_token

    async def create_refresh_token(self, user_login: str, auth: AuthJWT) -> str:
        refresh_token = await auth.create_refresh_token(
            subject=user_login,
            expires_time=self._access_token_ttl,
            algorithm=self._encryption_algorithm
        )
        return refresh_token

    async def refresh_token(
        self,
        auth: AuthJWT,
        redis_service: RedisService = get_redis_service()
    ) -> dict[str, str]:
        await auth.jwt_refresh_token_required()
        current_user = await auth.get_jwt_subject()
        new_access_token = await self.create_access_token(current_user, auth)
        new_refresh_token = await self.create_refresh_token(current_user, auth)
        jti = (await auth.get_raw_jwt())["jti"]

        entry = redis_service.get_token(jti)
        if entry:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token in revoke list")

        redis_service.revoke_token(jti)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    async def authenticate(
        self,
        auth: AuthJWT,
        login: str,
        redis_service: RedisService = get_redis_service()
    ) -> str:
        await auth.jwt_required()
        login_in_jwt = await auth.get_jwt_subject()
        jti = (await auth.get_raw_jwt())["jti"]
        entry = redis_service.get_token(jti)

        if entry:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token in revoke list")

        if login != login_in_jwt:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")

        return login

    async def logout(
        self,
        auth: AuthJWT,
        redis_service: RedisService = get_redis_service()
    ) -> None:
        await auth.jwt_refresh_token_required()
        jwt_data = await auth.get_raw_jwt()
        exp = jwt_data['exp']
        now = calendar.timegm(time.gmtime())
        redis_service.revoke_token(jwt_data['jti'], exp - now)


def get_security_service() -> SecurityService:
    return SecurityService(
        encryption_algorithm=settings.encryption_algorithm,
        access_token_ttl=settings.access_token_ttl,
        refresh_token_ttl=settings.refresh_token_ttl,
    )
