from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Text, CheckConstraint

from src.database import Base


class RatingsORM(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    rating: Mapped[int] = mapped_column(Integer, CheckConstraint('0 < rating <= 5'))
    rating_text: Mapped[int] = mapped_column(Text)
