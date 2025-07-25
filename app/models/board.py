from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .card import Card


class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        board = {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
        }

        return board


    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title = board_data["title"],
            owner = board_data["owner"],
        )
