from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData
from utils.case_converter import camel_case_to_snake_case
from core.config import settings


class Base(DeclarativeBase):
    __abstact__ = True

    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr
    def __tablename__(cls):
        return f"{camel_case_to_snake_case(cls.__name__)}s"
