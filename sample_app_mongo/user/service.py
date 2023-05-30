from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..auth import AuthService
from ..database import EnsureIndexes, get_database
from .models import SignupDTO, UserInDB
from pymongo import IndexModel, DESCENDING
from pymongo.errors import DuplicateKeyError

username_index_model = IndexModel([("username", DESCENDING)], unique=True)
username_index_ensure = EnsureIndexes("users", [username_index_model])


class UserService:

    def __init__(self,
                 db: Annotated[AsyncIOMotorDatabase,
                               Depends(get_database)],
                 auth: Annotated[AuthService, Depends()],
                 _ensured=Depends(username_index_ensure)):
        self.db = db
        self.auth = auth
        self.collection = self.db['users']

    async def create(self, user: SignupDTO):
        _user = jsonable_encoder(
            UserInDB(**user.dict(),
                     hashed_password=self.auth.get_password_hash(
                         user.password)))
        try:
            return await self.collection.insert_one(_user)
        except DuplicateKeyError:
            raise HTTPException(status_code=400,
                                detail="Username already exists")

    async def get(self, username: str):
        user = await self.collection.find_one({"username": username})
        if user:
            return UserInDB(**user)

    async def getById(self, id: str):
        user = await self.collection.find_one({"_id": id})
        if user:
            return UserInDB(**user)

    async def authenticate(self, username: str, password: str):
        user = await self.get(username)
        if not user:
            return None
        if not self.auth.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self,
                            data: dict,
                            expires_delta: timedelta | None = None):
        return self.auth.create_access_token(data, expires_delta)

    def validate_token(self, token: str):
        return self.auth.validate_token(token)