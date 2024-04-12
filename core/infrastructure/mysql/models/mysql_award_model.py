import base64
from struct import unpack
from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    LargeBinary,
    Float,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship, Mapped

from core.domain.entities.award import Award, AwardQualification
from core.infrastructure.mysql.models.mysql_base_model import MySQLBaseModel
from datetime import datetime


# MySQLAwardModel is a model that represents the awards table in the database
# This model is not used in the application, but it is used in the database
class MySQLAwardModel(MySQLBaseModel):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True, nullable=False)
    description = Column(String(length=1000), nullable=False)
    images: Mapped[List["MySQLAwardImageModel"]] = relationship("MySQLAwardImageModel")
    qualifications: Mapped[List["MySQLAwardQualificationModel"]] = relationship(
        "MySQLAwardQualificationModel"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @staticmethod
    def from_domain(award: Award) -> "MySQLAwardModel":
        return MySQLAwardModel(
            name=award.title,
            description=award.description,
            images=[MySQLAwardImageModel.from_domain(image) for image in award.images],
            qualifications=[
                MySQLAwardQualificationModel.from_domain(qualification)
                for qualification in award.qualification
            ],
        )

    def to_domain(self) -> Award:
        return Award(
            id=str(self.id),
            title=self.name,
            description=self.description,
            images=[image.to_domain() for image in self.images],
            qualification=[
                qualification.to_domain() for qualification in self.qualifications
            ],
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )


# MySQLAwardQualificationModel is a model that represents the award_qualifications table in the database
# This model is not used in the application, but it is used in the database
class MySQLAwardQualificationModel(MySQLBaseModel):
    __tablename__ = "award_qualifications"

    id = Column(Integer, primary_key=True, index=True)
    # Max 10. Ex 5.5, 7.5, 10 | Min 0. Ex 0, 2.5, 5
    qualification = Column(Float(precision=1, asdecimal=True, decimal_return_scale=1))
    award_id = Column(Integer, ForeignKey("awards.id"))
    user_email = Column(String(length=100))
    content = Column(String(length=1000))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    @staticmethod
    def from_domain(
        qualification: AwardQualification,
    ) -> "MySQLAwardQualificationModel":
        return MySQLAwardQualificationModel(
            qualification=qualification.qualification,
            user_email=qualification.user_email,
            content=qualification.content,
        )

    def to_domain(self) -> AwardQualification:
        return AwardQualification(
            id=str(self.id),
            qualification=self.qualification,
            user_email=self.user_email,
            created_at=self.created_at.isoformat(),
        )


# MySQLAwardImageModel is a model that represents the award_images table in the database
# This model is not used in the application, but it is used in the database
class MySQLAwardImageModel(MySQLBaseModel):
    __tablename__ = "award_images"

    id = Column(Integer, primary_key=True, index=True)
    # Max 4GB
    image = Column(LargeBinary, nullable=False)
    award_id = Column(
        Integer,
        ForeignKey(
            "awards.id",
        ),
        nullable=False,
    )

    @staticmethod
    def from_domain(image: bytes) -> "MySQLAwardImageModel":
        return MySQLAwardImageModel(image=image)

    def to_domain(self) -> bytes:
        image = base64.b64encode(self.image)
        return image
