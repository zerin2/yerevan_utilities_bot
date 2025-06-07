import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from db.models import *  # noqa
from db.models.base import Base
from settings import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# Функция для получения строки подключения
def get_url():
    return settings.database_url


# Функция для запуска миграций в режиме офлайн
def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )
    with context.begin_transaction():
        context.run_migrations()


# Функция для запуска миграций
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


# Асинхронная функция для запуска миграций в режиме онлайн
async def run_migrations_online():
    connectable = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


# Основная логика для определения режима работы
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
