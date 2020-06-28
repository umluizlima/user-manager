from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import Settings


@lru_cache
def get_session_maker(database_url: str):
    engine = create_engine(database_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Database:
    def __init__(self, settings: Settings):
        self._Session = get_session_maker(settings.DATABASE_URL)

    @contextmanager
    def get_session(self, autocommit=True):
        session = self._Session()
        try:
            yield session
            if autocommit:
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
