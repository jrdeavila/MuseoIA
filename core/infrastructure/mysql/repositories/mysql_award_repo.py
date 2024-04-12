from sqlalchemy import Engine, delete
from core.domain.entities.award import Award
from core.domain.repositories.award_repo import IAwardRepo
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.infrastructure.mysql.models.mysql_award_model import (
    MySQLAwardImageModel,
    MySQLAwardModel,
    MySQLAwardQualificationModel,
)


class MySQLAwardRepo(IAwardRepo):
    _engine: Engine

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def get_awards(self) -> list[Award]:
        session = Session(self._engine)
        stmt = select(MySQLAwardModel).order_by(MySQLAwardModel.created_at)
        items = session.execute(stmt).scalars().all()

        return [item.to_domain() for item in items]

    async def get_award(self, award_id: int) -> Award | None:
        session = Session(self._engine)
        stmt = select(MySQLAwardModel).where(MySQLAwardModel.id == award_id)
        item = session.execute(stmt).scalar()
        return item.to_domain() if item else None

    async def create_award(self, award: Award) -> Award:
        session = Session(self._engine)
        model = MySQLAwardModel.from_domain(award)
        session.add(model)
        session.commit()
        return model.to_domain()

    async def update_award(self, award_id: int, award: Award) -> Award | None:
        session = Session(self._engine)
        stmt = select(MySQLAwardModel).where(MySQLAwardModel.id == award_id)
        item = session.execute(stmt).scalar()
        if not item:
            return None
        item.name = award.title
        item.description = award.description
        item.images = [
            MySQLAwardImageModel.from_domain(image) for image in award.images
        ]
        item.qualifications = [
            MySQLAwardQualificationModel.from_domain(qualification)
            for qualification in award.qualification
        ]
        session.commit()

    async def delete_award(self, award_id: int) -> bool:
        session = Session(self._engine)
        stmt = delete(MySQLAwardModel).where(MySQLAwardModel.id == award_id)
        res = session.execute(stmt)
        if res.rowcount == 0:
            return False
        session.commit()
        return True
