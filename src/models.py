import sqlalchemy

from src.database import Base

USER_ID_SEQ = sqlalchemy.Sequence('user_id_seq')
users = sqlalchemy.Table(
    "users",
    Base.metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, USER_ID_SEQ, primary_key=True, server_default=USER_ID_SEQ),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)
