from sqlalchemy.orm import DeclarativeBase, declared_attr
from utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return f"{camel_case_to_snake_case(cls.__name__)}s"
