from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:oEoIQP0bOeIIulJBmEhT@containers-us-west-117.railway.app:5513/railway"
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
