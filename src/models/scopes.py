from enum import Enum


class Scope(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
