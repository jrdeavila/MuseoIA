import os

from sqlalchemy import Engine, create_engine

from core.application.services.learning_ia_award_service import LearningIAAwardService
from core.domain.repositories.award_repo import IAwardRepo
from core.domain.services.ia_award_service import IAAwardService
from core.domain.services.recognize_service import IRecognizeService
from core.infrastructure.mysql.models.mysql_base_model import MySQLBaseModel
from core.infrastructure.mysql.repositories.mysql_award_repo import MySQLAwardRepo
from core.infrastructure.opencv.services.opencv_reconize_service import (
    OpenCVRecognizeService,
)
from core.infrastructure.singleton.container import SingletonContainer


def create_MySQL_engine() -> Engine:
    HOST = "ls-9fc7b514b07427ef92190c2c480deb969b168d4d.cdwmpurkschl.us-east-1.rds.amazonaws.com"
    USERNAME = "learning_award_admin"
    PASSWORD = "learning_award_admin"
    DATABASE = "LEARNING_AWARD_DB"
    PORT = "3306"
    engine = create_engine(
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    )
    MySQLBaseModel.metadata.create_all(engine)
    return engine


async def configure_dependencies():

    SingletonContainer.register(
        Engine,
        create_MySQL_engine(),
    )
    SingletonContainer.register(
        IAwardRepo, MySQLAwardRepo(engine=SingletonContainer.resolve(Engine))
    )
    SingletonContainer.register(IRecognizeService, OpenCVRecognizeService())
    SingletonContainer.register(
        IAAwardService,
        LearningIAAwardService(
            award_repo=SingletonContainer.resolve(IAwardRepo),
            recognize_service=SingletonContainer.resolve(IRecognizeService),
        ),
    )
    print("Singletons configured.")
