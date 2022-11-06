import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BYTEA

from .database import Base


def generate_uuid():
    return str(uuid.uuid4())


# fastapi_users is not useful for User in this case
# SQLAlchemyBaseUserTableUUID has additional unnecessary required requirements: email, is_active, is_superuser, is_verified
class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # secret_key can be something deterministic on client side -> this key is used to encrypt the password using AES
    # since password is very light (small in size), we can use public key encryption with a deterministic secret_key
    secret_key = Column(String)
    subAccounts = relationship("SubAccount", back_populates="owner")


# Version 4: These are generated from random (or pseudo-random) numbers. If you just need to generate a UUID, this is probably what you want. The advantage of this version is that when you're debugging and looking at a long list of information matched with UUIDs, it's quicker to spot matches.
# Version 5: This generates a unique ID from an SHA-1 hash of a namespace and name. This is the more secure and generally recommended version.


class SubAccount(Base):
    __tablename__ = "subaccount"

    id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("user.id"))
    name = Column(String, index=True)
    data = Column(String)
    tag = Column(String)
    nonce = Column(String)

    owner = relationship("User", back_populates="subAccounts")
