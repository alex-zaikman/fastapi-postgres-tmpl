from typing import List

from fastapi import APIRouter, Depends, Security, Body, status

from auth import validate_token_data, get_hash
from database import DataBase
from models.scopes import Scope
from models.token import TokenData
from models.users import NewUser, DisplayUser
from schema.users import users

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/", response_model=List[DisplayUser], description='List users.')
async def list_users(session=Depends(DataBase().get_session),
                     token: TokenData = Security(validate_token_data,  # pylint: disable=unused-argument
                                                 scopes=[Scope.ADMIN, Scope.USER])
                     ):
    query = users.select()
    result = await session.execute(query)
    return result.all()


@router.post("/", status_code=status.HTTP_201_CREATED, description='Add new user')
async def create_new_user(session=Depends(DataBase().get_session),
                          new_user: NewUser = Body(...),
                          token: TokenData = Security(validate_token_data, scopes=[Scope.ADMIN])  # pylint: disable=unused-argument
                          ):
    query_params = new_user.dict()
    query_params.pop('id', None)  # ensure id is not passed.
    query_params['password'] = get_hash(query_params['password'])  # hash password
    query = users.insert().values(**query_params)
    await session.execute(query)
