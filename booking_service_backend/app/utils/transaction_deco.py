from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

def transaction(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: AsyncSession = kwargs.get("session")
        if not session or not isinstance(session, AsyncSession):
            raise ValueError("Session must be set or must be type 'AsyncSession'")
        
        try:
            res = await func(*args, **kwargs)
            await session.commit()
            return res
        
        except Exception as e:
            await session.rollback()
            print(e)
            raise e
    
    return wrapper
            