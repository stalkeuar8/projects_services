from typing import Coroutine
import asyncio


class BackgroundTaskObserver:

    def __init__(self, tasks: set[Coroutine]):
        self.inactive_tasks: set[Coroutine] = tasks
        self.active_tasks: set[asyncio.Task] = set()


    async def __aenter__(self):
        for task in self.inactive_tasks:
            self.active_tasks.add(asyncio.create_task(task))
        self.inactive_tasks = set()

        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        for task in self.active_tasks:
            task.cancel()

        await asyncio.gather(*self.active_tasks, return_exceptions=True)
        self.active_tasks = set()

        if exc_type is not None:
            print(f'\nError occured: {exc}. Background tasks canceled.')

        print(f'\nBackground tasks canceled.')

        return True