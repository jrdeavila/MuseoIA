from pydantic import BaseModel, Field


class CreateAwardRequest(BaseModel):
    title: str = Field(
        ...,
        title="Title of the award",
        description="Title of the award",
        min_length=1,
        max_length=200,
    )
    description: str = Field(
        ...,
        title="Description of the award",
        description="Description of the award",
        min_length=1,
        max_length=1000,
    )
