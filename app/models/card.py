from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .board import Board


class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="cards")



    def to_dict(self):
        card = {
            "id": self.card_id,
            "message": self.message,
            "likes": self.likes_count,
        }

        return card


    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message = card_data["message"],
            likes_count = card_data.get("likes", 0),
            board_id = card_data["board_id"],
        )
