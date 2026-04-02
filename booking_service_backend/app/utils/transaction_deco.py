# from functools import wraps
# from typing import Any, Callable

# from sqlalchemy.ext.asyncio import AsyncSession

# from app.settings.database import async_session_factory




# def transaction(func: Callable) -> Callable:
#     @wraps(func)
#     async def wrapper(**kwargs) -> Any:
#         session: AsyncSession | None = kwargs.get("session")

#         if session and isinstance(session, AsyncSession):
#             return await func(**kwargs)

#         async with async_session_factory() as new_session:
#             try:
#                 kwargs["session"] = new_session

#                 res = await func(**kwargs)

#                 await new_session.commit()
#                 return res

#             except Exception as e:
#                 await new_session.rollback()
#                 print(f"{func.__name__} error: {e}")
#                 raise e

#     return wrapper
