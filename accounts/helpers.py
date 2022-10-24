from fastapi import Depends, HTTPException, status
from database.helpers import get_async_session
from sqlalchemy import select, update
from sqlalchemy.orm import Session

# Db models
from database.models import User
from database.helpers import pwd_context


async def get_user(username: str, db: Session = Depends(get_async_session)):
    query = select(User).where(User.username == username)
    result = (await db.scalars(query)).first()
    return result


async def validate_user(
    username: str, password: str, db: Session = Depends(get_async_session)
):
    result = await get_user(username, db)

    if not result:
        return None
    elif verify_password(plain_password=password, hashed_password=result.password):
        return result
    else:
        return None


async def new_user(
    username: str, password: str, db: Session = Depends(get_async_session)
):
    hashedPassword = get_password_hash(password)

    result = await get_user(username, db)

    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration unsuccessful, username in use",
        )

    new_user = User(username=username, password=hashedPassword)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def update_password(
    username: str, newPassword: str, db: Session = Depends(get_async_session)
):
    hashedNewPassword = get_password_hash(newPassword)
    update_query = (
        update(User).values(password=hashedNewPassword).where(User.username == username)
    )
    await db.execute(update_query)
    await db.commit()

    new_result = await get_user(username, db)
    return new_result


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)
