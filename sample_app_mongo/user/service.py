from datetime import timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..auth import AuthService
from ..database import get_database
from .models import User, UserInDB


class UserService:

    def __init__(self, db: Annotated[AsyncIOMotorDatabase,
                                     Depends(get_database)],
                 auth: Annotated[AuthService, Depends()]):
        self.db = db
        self.auth = auth
        self.collection = self.db['users']

    async def create(self, user: User) -> UserInDB:
        user = jsonable_encoder(
            UserInDB(**user.dict(),
                     hashed_password=self.auth.get_password_hash(
                         user.password)))
        return await self.collection.insert_one(user.dict())

    async def get(self, username: str):
        return await self.collection.find_one({"username": username})

    async def authenticate(self, username: str, password: str):
        user = await self.get(username)
        if not user:
            return False
        if not self.auth.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self,
                            data: dict,
                            expires_delta: timedelta | None = None):
        return self.auth.create_access_token(data, expires_delta)

    def validate_token(self, token: str):
        return self.auth.validate_token(token)


def get_user_service():
    return UserService()