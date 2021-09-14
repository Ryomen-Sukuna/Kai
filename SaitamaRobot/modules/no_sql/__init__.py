"""MongoDB Database."""

from odmantic import AIOEngine
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, collection
from pymongo.errors import ServerSelectionTimeoutError
from SaitamaRobot import (
    LOGGER,
    MONGO_URI,
    MONGO_DB,
    MONGO_PORT,
)

LOGGER.info("Connecting to MongoDB")
LOGGER.info("MongoDB Connected")

mongodb = MongoClient(MONGO_URI, MONGO_PORT)[MONGO_DB]
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.KaiRobot
engine = AIOEngine(mongo_client, MONGO_DB)
DB_CLIENT = MongoClient(MONGO_URI)
_DB = DB_CLIENT["KaiRobot"]


def get_collection(name: str) -> collection:
    """Get the collection from database."""
    return _DB[name]
