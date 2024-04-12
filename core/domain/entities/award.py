from pydantic import BaseModel, Field


class Award(BaseModel):
    id: str | None = Field(None, title="ID of the award")
    title: str = Field(..., title="Title of the award")
    description: str = Field(..., title="Description of the award")
    images: list[bytes]
    qualification: list["AwardQualification"] = []
    created_at: str | None = Field(None, title="Date and time the award was created")
    updated_at: str | None = Field(None, title="Date and time the award was updated")


class AwardQualification(BaseModel):
    id: str = Field(..., title="ID of the qualification")
    qualification: float = Field(..., title="Qualification of the award")
    user_email: str = Field(..., title="Email of the user that qualified the award")
    created_at: str = Field(..., title="Date and time the qualification was created")
