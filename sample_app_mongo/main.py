from fastapi import FastAPI

from .user.controllers import router as user_router

from .form_data.controllers import router as form_data_router

app = FastAPI()

app.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
)

app.include_router(
    form_data_router,
    prefix="/form_data",
    tags=["forms"],
)