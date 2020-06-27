from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import get_settings


@lru_cache
def get_session_maker():
    settings = get_settings()
    engine = create_engine(settings.DATABASE_URL)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    Session = get_session_maker()
    try:
        session = Session()
        yield session
        session.commit()
    except Exception as error:
        session.rollback()
        raise error
    finally:
        session.close()
