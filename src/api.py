import logging

import uvicorn
from fastapi import FastAPI, Depends, status, Response, Security, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from auth import create_refresh_token, create_access_token, validate_refresh_token_data
from auth import verify_hashed
from database import DataBase
from endpoints import user_api
from middleware import ContextIdMiddleware, TimeMiddleware
from models.token import TokenData, Token
from models.users import User
from schema.users import get_db_user

logger = logging.getLogger("api")
app = FastAPI(title="Demo app.", version='1.0.0', description="FastAPI and postgres demo.")

app.include_router(user_api.router)

app.add_middleware(TimeMiddleware)
app.add_middleware(ContextIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[TimeMiddleware.HEADER_NAME, ContextIdMiddleware.HEADER_NAME]
)


@app.on_event("startup")
async def startup():
    DataBase()  # warmup db connection


# @app.on_event("shutdown")
# def shutdown_db_client():
#     pass


@app.get("/ping")
async def ping(bt: BackgroundTasks,
               context_id: str = Depends(ContextIdMiddleware.get_context)):
    bt.add_task(logger.debug, "ping", extra={"context_id": context_id})
    return Response(status_code=status.HTTP_200_OK)


@app.get("/")
async def redirect_root():  # pragma: no cover
    """Reroutes the default path to docs"""
    return RedirectResponse("/docs")


@app.post('/refresh', tags=['Auth'], response_model=Token)
async def refresh(bt: BackgroundTasks, session=Depends(DataBase().get_session),
                  context_id: str = Depends(ContextIdMiddleware.get_context),
                  token: TokenData = Security(validate_refresh_token_data),
                  ):
    bt.add_task(logger.info, f'Getting token and refresh for {token.user.email}',
                extra={"context_id": context_id})

    _user = await get_db_user(session=session, email=token.user.email)

    refresh_token = create_refresh_token(data=User.from_orm(_user).dict())
    access_token = create_access_token(data=User.from_orm(_user).dict())

    bt.add_task(logger.info, f'Login succeeded for {token.user.email}',
                extra={"context_id": context_id})

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


@app.post('/token', tags=['Auth'], response_model=Token)
async def get_token(bt: BackgroundTasks,
                    context_id: str = Depends(ContextIdMiddleware.get_context),
                    session=Depends(DataBase().get_session),
                    form_data: OAuth2PasswordRequestForm = Depends()):
    bt.add_task(logger.info, f'Getting token for {form_data.username}',
                extra={"context_id": context_id})

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"})

    _user = await get_db_user(session=session, email=form_data.username)

    if not _user or not verify_hashed(plain=form_data.password, hashed=_user.password):
        bt.add_task(logger.warning,
                    f'Illegal password for {form_data.username}',
                    extra={"context_id": context_id})
        raise exception

    refresh_token = create_refresh_token(data=User.from_orm(_user).dict())
    access_token = create_access_token(data=User.from_orm(_user).dict())

    bt.add_task(logger.info, f'Login succeeded for {form_data.username}',
                extra={"context_id": context_id})

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


if __name__ == '__main__':
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8001,
                log_config="logger.json",
                log_level=logging.DEBUG)
