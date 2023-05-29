from fastapi import Depends, FastAPI


from .user.controllers import router as user_router

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["users"])