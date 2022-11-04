from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:VBbmoRml8Gsu3C211E3x@containers-us-west-105.railway.app:7870/railway"
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
