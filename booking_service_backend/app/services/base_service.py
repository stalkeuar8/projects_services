from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService(ABC):

    @abstractmethod
    async def prepare_dto(self, short_dto: BaseModel, session: AsyncSession):
        pass