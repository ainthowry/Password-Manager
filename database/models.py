from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    password = Column(String)

    subAccounts = relationship("SubAccount", back_populates="owner")


class SubAccount(Base):
    __tablename__ = "subaccounts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    password = Column(String)

    owner = relationship("User", back_populates="subAccounts")
