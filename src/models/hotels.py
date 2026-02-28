from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, UniqueConstraint, CheckConstraint

from src.database import Base


class HotelsORM(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String)

    __table_args__ = (UniqueConstraint('title', 'location', name='_title_location_uc'),)
