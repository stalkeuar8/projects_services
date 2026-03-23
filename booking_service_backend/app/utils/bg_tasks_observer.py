import asyncio
from types import TracebackType
from typing import Coroutine, Self, Type


# class BackgroundTaskObserver:
#     def __init__(self, tasks: set[Coroutine]) -> None:
#         self.inactive_tasks: set[Coroutine] = tasks
#         self.active_tasks: set[asyncio.Task] = set()

#     async def __aenter__(self) -> Self:
#         for task in self.inactive_tasks:
#             self.active_tasks.add(asyncio.create_task(task))
#         self.inactive_tasks = set()

#         return self

#     async def __aexit__(self, exc_type: Type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> bool:
#         for task in self.active_tasks:
#             task.cancel()

#         await asyncio.gather(*self.active_tasks, return_exceptions=True)
#         self.active_tasks = set()

#         if exc_type is not None:
#             # example (remove in prod)
#             print(f"\nError occured: {exc}. Background tasks canceled.")

#         # example (remove in prod)
#         print("\nBackground tasks canceled.")

#         return True
