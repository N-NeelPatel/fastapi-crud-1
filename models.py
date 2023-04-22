from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import ARRAY


class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    edition = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=False)
    authors = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
