from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint, Float

from src.database import Base


class HotelsORM(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String)
    stars: Mapped[int]
    rating: Mapped[float] = mapped_column(Float, default=0.0)

    __table_args__ = (UniqueConstraint('title', 'location', name='_title_location_uc'),)
