# stdlib
import asyncio
from logging.config import fileConfig

# thirdparty
from sqlalchemy.ext.asyncio import create_async_engine

# project
from alembic import context
from src.config import settings
from src.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    engine = create_async_engine(settings.DB_URL, echo=True)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context."""

    asyncio.run(run_async_migrations())


run_migrations_online()
