from app import db, create_app
from app.models.board import Board
from app.models.card import Card

def seed_data():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

    # Create boards
    ada_board = Board(title="Ada Inspiration", owner="Ada Lovelace")
    nerd_board = Board(title="Nerdy Dev Jokes", owner="Grace Hopper")
    wellness_board = Board(title="Wellness & Mindfulness", owner="Alan Turing")

    db.session.add_all([ada_board, nerd_board, wellness_board])
    db.session.commit()

    # Cards for Ada Board
    ada_cards = [
        Card(message="You’ve got this! One line at a time. 🧠💪", likes_count=3, board_id=ada_board.id),
        Card(message="Every bug you squash is a step forward 🐞➡️🚫", likes_count=5, board_id=ada_board.id),
        Card(message="Push yourself, not just your code. 🚀", likes_count=2, board_id=ada_board.id),
    ]

    # Cards for Nerdy Dev Jokes Board
    nerd_cards = [
        Card(message="Why do programmers hate nature? It has too many bugs! 🌳😆", likes_count=7, board_id=nerd_board.id),
        Card(message="To understand recursion, you must first understand recursion.", likes_count=6, board_id=nerd_board.id),
        Card(message="I told my computer I needed a break, and it said '404: Motivation Not Found' 💻💤", likes_count=4, board_id=nerd_board.id),
    ]

    # Cards for Wellness Board
    wellness_cards = [
        Card(message="Breathe in confidence. Breathe out doubt. 🌬️💖", likes_count=3, board_id=wellness_board.id),
        Card(message="It’s okay to rest. Even servers need to reboot. 😴🔁", likes_count=5, board_id=wellness_board.id),
        Card(message="You are more than your code output. 🌈", likes_count=2, board_id=wellness_board.id),
    ]

    db.session.add_all(ada_cards + nerd_cards + wellness_cards)
    db.session.commit()

    print("🌟 Seed data loaded!")

if __name__ == "__main__":
    seed_data()
