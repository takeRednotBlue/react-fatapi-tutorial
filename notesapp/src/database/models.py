from datetime import datetime
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.database.db import engine


def timestamp_now():
    return round(datetime.now().timestamp())


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4(), unique=True)
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=timestamp_now())
    updated_at: Mapped[datetime] = mapped_column(default=timestamp_now())


Base.metadata.create_all(bind=engine)
