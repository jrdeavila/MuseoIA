from typing import Union
from core.domain.entities.award import Award


class IAwardRepo:
    async def get_awards(self) -> list[Award]:
        raise NotImplementedError()

    async def get_award(self, award_id: int) -> Union[Award, None]:
        raise NotImplementedError()

    async def create_award(self, award: Award) -> Award:
        raise NotImplementedError()

    async def update_award(self, award_id: int, award: Award) -> Union[Award, None]:
        raise NotImplementedError()

    async def delete_award(self, award_id: int) -> bool:
        raise NotImplementedError()
