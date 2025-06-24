from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db



class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    board_id: Mapped[Mapped[int]] = mapped_column(default=None)
    board: Mapped[Mapped["Card"]] = relationship(back_populates="cards")
