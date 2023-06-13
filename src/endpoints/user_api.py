from typing import List

from fastapi import APIRouter, Depends, Security, Body, status
from sqlalchemy import insert

from src.auth import validate_token_data
from src.database import get_session
from src.models.token import TokenData
from src.models.scopes import Scope
from src.models.users import UserBase, NewUser
from src.schema.users import users, USER_ID_SEQ

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/", response_model=List[UserBase])
async def list_users(session=Depends(get_session),
                     token: TokenData = Security(validate_token_data,
                                                 scopes=[Scope.ADMIN, Scope.USER])):  # pylint: disable=unused-argument
    query = users.select()
    result = await session.execute(query)
    return result.all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(session=Depends(get_session),
                          new_user: NewUser = Body(...),
                          # token: TokenData = Security(validate_token_data, scopes=[Scope.ADMIN])  # pylint: disable=unused-argument
                          ):
    query_params = new_user.dict()
    query_params.pop('id', None)
    query = users.insert().values(**query_params)
    await session.execute(query)
