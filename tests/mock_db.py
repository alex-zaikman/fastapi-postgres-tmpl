import os

import psycopg
import testing.postgresql

from singleton_meta import SingletonMeta


class _Postgresql(metaclass=SingletonMeta):
    def __init__(self):
        self.__postgresql = self._postgres_factory()

    @staticmethod
    def _init_db(db):
        os.environ.setdefault('DB_NULL_POOL', 'true')
        os.environ.setdefault('DB_ECHO', 'true')
        conn = psycopg.connect(db.url())
        cur = conn.cursor()

        with open(os.path.join(os.path.dirname(__file__), '../db/init.sql'), 'r', encoding="UTF-8") as fp:
            _ = [(cur.execute(statement.strip())) for statement in fp.read().split(';') if statement.strip()]

        conn.commit()
        cur.close()
        conn.close()

    def _postgres_factory(self):
        """
        Creates an initial fake database for use in unit tests.
        """
        postgres_factory = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                                on_initialized=self._init_db)
        return postgres_factory

    def __call__(self, *args, **kwargs):
        return self.__postgresql()

    def clear_cache(self):
        self.__postgresql.clear_cache()


Postgresql = _Postgresql()
