from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .service import UserService

from .models import SignupDTO, TokenDTO, User, UserInDB

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_service():
    return UserService()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], service: Annotated[UserService, Depends()]):
    token_data = service.verify_token(token)
    user = await service.get(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabrabbitled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/signup/")
async def signup(user: SignupDTO, db: Depends(get_service)):
    result = await db.create(user)
    return result


@router.post("/token", response_model=TokenDTO)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,
                                                      Depends()],
                                 service: Annotated[UserService,
                                                    Depends()]):
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user