from typing import Annotated
from fastapi import Depends
from motor import motor_asyncio
from .config import get_settings, Settings



def get_database(config: Annotated[Settings, Depends(get_settings)]):
    client = motor_asyncio.AsyncIOMotorClient(config.mongo_url)

    db =  client['sample_app_db']
    return db