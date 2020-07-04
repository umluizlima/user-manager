from os import environ, system

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.core.database import Database
from app.core.models.base import Base
from tests.conftest import get_test_settings


@fixture(scope="session", autouse=True)
def db():
    environ["POSTGRES_DB"] = "user-manager"
    postgres_container = PostgresContainer("postgres:12.2-alpine")
    with postgres_container as postgres:
        environ["DATABASE_URL"] = postgres.get_connection_url()
        database = Database(get_test_settings())
        system("alembic upgrade head")
        yield database


@fixture
def db_session(db: Database):
    with db.get_session() as session:
        try:
            yield session
        finally:
            session.rollback()
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()
            session.close()


@fixture(scope="session", autouse=True)
def cache_client():
    redis_container = RedisContainer("redis:6.0.5-alpine")
    with redis_container as redis:
        yield redis.get_client()
