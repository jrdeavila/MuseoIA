from fastapi import APIRouter, Depends, File, Form, UploadFile

from api.requests import CreateAwardRequest
from core.domain.entities.award import Award
from core.domain.services.ia_award_service import IAAwardService
from core.infrastructure.singleton.container import SingletonContainer


router = APIRouter()


def get_ia_award_service() -> IAAwardService:
    return SingletonContainer.resolve(IAAwardService)


@router.get("/awards/", tags=["Awards"], response_model=list[Award])
async def get_awards(
    award_service: IAAwardService = Depends(get_ia_award_service),
):
    return await award_service.get_awards()


@router.post("/recognize/awards/", tags=["Awards"], response_model=Award)
async def recognize_awards(
    file: UploadFile = File(
        title="File to recognize awards from",
        description="File to recognize awards from",
    ),
    award_service: IAAwardService = Depends(get_ia_award_service),
):
    return await award_service.recognize(await file.read())


@router.post("/learning/awards/", tags=["Awards"], response_model=Award)
async def create_award(
    files: list[UploadFile] = File(
        ...,
        title="Files to learn the award from",
        description="Files to learn the award from",
    ),
    title: str = Form(
        ...,
        title="Title of the award",
        description="Title of the award",
        min_length=1,
        max_length=200,
    ),
    description: str = Form(
        ...,
        title="Description of the award",
        description="Description of the award",
        min_length=1,
        max_length=1000,
    ),
    award_service: IAAwardService = Depends(get_ia_award_service),
):
    return await award_service.learn(
        title=title,
        description=description,
        files=[await file.read() for file in files],
    )


@router.get("/")
async def root():
    return {
        "message": "Welcome to the Museo el Cocha Molina API",
    }
