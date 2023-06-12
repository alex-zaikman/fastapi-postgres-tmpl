import logging
import os
import string
import hashlib
from random import choice
from datetime import datetime, timedelta

from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from jose import JWTError, jwt
from jose.constants import ALGORITHMS

from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from src.models import TokenData, TokenType, User

# Auth conf
API_ALGORITHM = os.environ.get("API_ALGORITHM", ALGORITHMS.HS256)
API_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("API_ACCESS_TOKEN_EXPIRE_MINUTES", 15)
API_REFRESH_TOKEN_EXPIRE_DAYS = os.environ.get("API_REFRESH_TOKEN_EXPIRE_DAYS", 30)
API_SECRET_KEY = os.environ.get("API_SECRET_KEY",
                                hashlib.sha512(''.join(choice(string.ascii_letters)
                                                       for i in range(29)).encode()).hexdigest())
API_REFRESH_SECRET_KEY = os.environ.get("API_REFRESH_SECRET_KEY",
                                        hashlib.sha512(''.join(choice(string.ascii_letters)
                                                               for i in range(29)).encode()).hexdigest())

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger("api")


def verify_hashed(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def get_hash(str_to_hash: str) -> str:
    """

    :rtype: object
    """
    return _pwd_context.hash(str_to_hash)


async def validate_token_data(security_scopes: SecurityScopes, token__: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
    )

    # parse token payload
    try:
        payload = jwt.decode(token__, API_SECRET_KEY, algorithms=[API_ALGORITHM])
    except JWTError as exc:
        raise credentials_exception from exc

    return await validate_token(token__, payload, credentials_exception, security_scopes)


async def validate_refresh_token_data(token__: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f'Bearer token="{token__}"'},
    )
    # parse token payload
    try:
        payload = jwt.decode(token__, API_REFRESH_SECRET_KEY, algorithms=[API_ALGORITHM])
    except JWTError as exc:
        raise credentials_exception from exc

    return await validate_token(token__, payload, credentials_exception)


async def validate_token(token__, payload, credentials_exception, security_scopes=None):
    if security_scopes:
        # validate Scopes
        if not all(scope in payload['scopes'] for scope in security_scopes.scopes):
            raise credentials_exception

    # # validate against db
    # try:
    #     dbuser = DBUser.objects.get(email=payload['email'])
    # except DoesNotExist as exc:
    #     raise credentials_exception from exc
    #
    # if security_scopes:
    #     if set(dbuser.scopes) != set(payload['scopes']):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="insufficient privileges",
    #             headers={"WWW-Authenticate": f'Bearer token="{token__}"'},
    #         )
    #
    # if payload['token_title'] == TokenType.REFRESH:
    #     if not verify_hashed(token__, dbuser.refresh_token):
    #         raise credentials_exception
    #
    # if payload['token_title'] == TokenType.ACCESS:
    #     if not verify_hashed(token__, dbuser.access_token):
    #         raise credentials_exception

    return TokenData(user=User(**payload), exp=payload['exp'])


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=int(API_ACCESS_TOKEN_EXPIRE_MINUTES))
    data['token_title'] = TokenType.ACCESS
    encoded_jwt = jwt.encode({"exp": expire, **data}, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=int(API_REFRESH_TOKEN_EXPIRE_DAYS))
    data['token_title'] = TokenType.REFRESH
    encoded_jwt = jwt.encode({"exp": expire, **data}, API_REFRESH_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


def get_context(request: Request) -> str:
    return request.state.context_id


def get_logger(bt: BackgroundTasks,
               context_id: str = Depends(get_context)):
    return lambda msg, func=logger.info: bt.add_task(func, msg, extra={"context_id": context_id})


if __name__ == '__main__':
    print(get_hash('alex123'))