from sqlalchemy.orm import DeclarativeBase


class MySQLBaseModel(DeclarativeBase):
    __abstract__ = True
