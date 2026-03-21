from functools import wraps
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import async_session_factory


def transaction(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: AsyncSession | None = kwargs.get("session")

        if session and isinstance(session, AsyncSession):
            return await func(*args, **kwargs)

        async with async_session_factory() as new_session:
            try:
                kwargs["session"] = new_session

                res = await func(*args, **kwargs)

                await new_session.commit()
                return res

            except Exception as e:
                await new_session.rollback()
                print(f"{func.__name__} error: {e}")
                raise e

    return wrapper
