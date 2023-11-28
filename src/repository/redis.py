from redis import Redis

from core import settings


class RedisService:
    def __init__(self):
        self.conn = Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)

    def get_token(self, token):
        return self.conn.get(token)

    def revoke_token(self, token: str, expire: int = settings.access_token_ttl):
        self.conn.setex(token, expire, "true")


def get_redis_service():
    return RedisService()
