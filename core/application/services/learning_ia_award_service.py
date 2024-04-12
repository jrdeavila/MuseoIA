from core.application.exceptions.exception import NotFound
from core.domain.entities.award import Award
from core.domain.repositories.award_repo import IAwardRepo
from core.domain.services.ia_award_service import IAAwardService
from core.domain.services.recognize_service import IRecognizeService


class LearningIAAwardService(IAAwardService):

    _award_repo: IAwardRepo
    _recognize_service: IRecognizeService

    def __init__(
        self, award_repo: IAwardRepo, recognize_service: IRecognizeService
    ) -> None:
        self._award_repo = award_repo
        self._recognize_service = recognize_service

    async def recognize(self, image: bytes) -> Award:
        all_awards = await self._award_repo.get_awards()

        for award in all_awards:
            if await self._recognize_service.recognize(award.images, image):
                return award

        raise NotFound(
            message="Award not found",
        )

    async def learn(self, title: str, description: str, files: list[bytes]) -> Award:
        return await self._award_repo.create_award(
            Award(title=title, description=description, images=files)
        )

    async def get_awards(self) -> list[Award]:
        return await self._award_repo.get_awards()
