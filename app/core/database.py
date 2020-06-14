from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import settings

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        session = Session()
        yield session
        session.commit()
    except Exception as error:
        session.rollback()
        raise error
    finally:
        session.close()
