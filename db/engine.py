from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://your_user_name:your_password@localhost:5432/your_db_name"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()
