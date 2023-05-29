from typing import Annotated
from fastapi import Depends, FastAPI

from .user.service import UserService

from .user.models import SignupDTO



app = FastAPI()


def get_service():
    return UserService()

@app.post("/signup/")
async def signup(user: SignupDTO, db: Annotated[UserService, Depends(get_service)]):
    result = await db.create(user)
    return result