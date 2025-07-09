from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .board import Board
from random import randint


class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        colors = [
            '#db96b9',
            '#e4a8b9',
            '#c8a8d5',
            '#d2ccf2',
            '#f2d2cc',
            '#e4eeff',
            ]

        randomColor = randint(0, 5)

        card = {
            "id": self.id,
            "message": self.message,
            "likes": self.likes_count,
            "color": colors[randomColor]
        }
        if self.image_url:
            card["image"] = self.image_url

        return card

    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message = card_data["message"],
            likes_count = card_data.get("likes", 0),
            image_url = card_data.get("image_url"),
            board_id = card_data["board_id"],
        )
