from os import getenv

from redis_pal import RedisPal


def get_skupper_redis_client() -> RedisPal:
    host = getenv("SKUPPER_REDIS_HOST")
    port = int(getenv("SKUPPER_REDIS_PORT"))
    db = int(getenv("SKUPPER_REDIS_DB"))
    password = getenv("SKUPPER_REDIS_PASSWORD")
    return RedisPal(host=host, port=port, db=db, password=password)
