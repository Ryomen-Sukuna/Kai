"""Redis Database."""

from redis import StrictRedis
from SaitamaRobot import LOGGER, REDIS_URL

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
LOGGER.info("Connecting RedisDB")
LOGGER.info("RedisDB Connected")
