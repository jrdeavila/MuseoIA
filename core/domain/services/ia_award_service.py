from core.domain.entities.award import Award


class IAAwardService:
    async def recognize(self, image: bytes) -> Award:
        raise NotImplementedError()

    async def learn(self, title: str, description: str, files: list[bytes]) -> Award:
        raise NotImplementedError()

    async def get_awards(self) -> list[Award]:
        raise NotImplementedError()
