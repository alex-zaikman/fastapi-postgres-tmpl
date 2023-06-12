import logging
import time
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, Request, status, Response, Security, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from src.auth import validate_token_data, verify_hashed
from src.auth import create_refresh_token, create_access_token, validate_refresh_token_data
from src.database import engine, Base, get_session
from src.models.token import TokenData, Scope, Token
from src.models.users import User, UserBase
from src.schema.users import users, get_db_user

logger = logging.getLogger("api")
app = FastAPI(title="Demo app.", version='1.0.0', description="FastAPI and postgres demo.")


class TimeMiddleware(BaseHTTPMiddleware):
    """This middleware adds "X-Process-Time" header with server code execution time."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
        return response


app.add_middleware(TimeMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"]
)


@app.on_event("startup")
async def startup():
    """Alchemy create all on server startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# @app.on_event("shutdown")
# def shutdown_db_client():
#     pass

@app.get("/ping")
async def ping(bt: BackgroundTasks):
    bt.add_task(logger.debug, "ping")
    return Response(status_code=status.HTTP_200_OK)


@app.get("/")
async def redirect_root():  # pragma: no cover
    """Reroutes the default path to docs"""
    return RedirectResponse("/docs")


@app.get("/user/list", response_model=List[UserBase])
async def list_users(session=Depends(get_session),
                     token: TokenData = Security(validate_token_data, scopes=[Scope.USER])):  # pylint: disable=unused-argument
    query = users.select()
    result = await session.execute(query)
    return result.all()


@app.post('/refresh', response_model=Token)
async def refresh(bt: BackgroundTasks, session=Depends(get_session),
                  token: TokenData = Security(validate_refresh_token_data),
                  ):
    bt.add_task(logger.info, f'Getting token and refresh for {token.user.email}')

    _user = await get_db_user(session=session, email=token.user.email)

    refresh_token = create_refresh_token(data=User.from_orm(_user).dict())
    access_token = create_access_token(data=User.from_orm(_user).dict())

    bt.add_task(logger.info, f'Login succeeded for {token.user.email}')

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


@app.post('/token', response_model=Token)
async def get_token(bt: BackgroundTasks,
                    session=Depends(get_session),
                    form_data: OAuth2PasswordRequestForm = Depends()):
    bt.add_task(logger.info, f'Getting token for {form_data.username}')

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"})

    _user = await get_db_user(session=session, email=form_data.username)

    if not verify_hashed(plain=form_data.password, hashed=_user.password):
        bt.add_task(logger.warning,
                    f'Illegal password for {form_data.username}')
        raise exception

    refresh_token = create_refresh_token(data=User.from_orm(_user).dict())
    access_token = create_access_token(data=User.from_orm(_user).dict())

    bt.add_task(logger.info, f'Login succeeded for {form_data.username}')

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8001,
                log_level=logging.DEBUG)
