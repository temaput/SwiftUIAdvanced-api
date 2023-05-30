from typing import Annotated
from bson import ObjectId
from fastapi import Depends
from motor import motor_asyncio
from pymongo import IndexModel
from .config import get_settings, Settings


def get_database(config: Annotated[Settings, Depends(get_settings)]):
    client = motor_asyncio.AsyncIOMotorClient(config.mongo_url)

    db = client['sample_app_db']
    return db


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class EnsureIndexes:

    def __init__(self, collection: str, indexes: list[IndexModel]):
        self.collection = collection
        self.indexes = indexes
        self.was_called = False

    async def __call__(self, db: Annotated[motor_asyncio.AsyncIOMotorDatabase,
                                           Depends(get_database)]):
        if not self.was_called:
            print("Creating index")
            await db[self.collection].create_indexes(self.indexes)
            self.was_called = True
