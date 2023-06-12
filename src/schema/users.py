import sqlalchemy
from sqlalchemy import text

from src.database import Base

USER_ID_SEQ = sqlalchemy.Sequence('user_id_seq')

users = sqlalchemy.Table(
    "users",
    Base.metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, USER_ID_SEQ,
                      primary_key=True,
                      server_default=text("NEXT VALUE FOR user_id_seq")),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("scopes", sqlalchemy.ARRAY(sqlalchemy.String)),
)


async def get_db_user(session, email):
    query = users.select().where(users.c.email == email.lower())
    _user = await session.execute(query)
    _user = _user.first()
    return _user