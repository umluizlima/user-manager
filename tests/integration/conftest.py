from os import environ, system

from pytest import fixture
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from app.core.adapters import CacheAdapter
from app.core.database import Database
from app.core.models.base import Base
from app.core.repositories import UsersRepository
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
        host = redis.get_container_host_ip()
        port = redis.get_exposed_port(6379)
        environ["CACHE_URL"] = f"redis://:@{host}:{port}/0"
        yield redis.get_client()


@fixture
def cache_adapter(cache_client):
    return CacheAdapter(cache_client)


@fixture
def users_repository(db_session):
    return UsersRepository(db_session)
