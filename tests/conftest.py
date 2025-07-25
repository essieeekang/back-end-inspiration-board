from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
from app.models.board import Board
from app.models.card import Card
from unittest.mock import patch
from io import BytesIO
import pytest
import os


load_dotenv()


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": (
            os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")),
    }

    app = create_app(test_config)


    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app


    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def single_card(app):
    new_card = Card(message="Have a great day!",
                    likes_count=0,
                    board_id=1)

    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def five_cards(app):
    db.session.add_all([
        Card(message="Have a great day!",
            likes_count=0,
            board_id=1),
        Card(message="Test msg!",
            likes_count=0,
            board_id=1),
        Card(message="You're doing great!!",
            likes_count=0,
            board_id=1),
        Card(message="Eat a cookie!",
            likes_count=0,
            board_id=1),
        Card(message="Take a break!",
            likes_count=0,
            board_id=1),
    ])
    db.session.commit()


@pytest.fixture
def three_cards_with_likes(app):
    db.session.add_all([
        Card(message="Have a great day!",
            likes_count = 3,
            board_id = 1),
        Card(message="Test msg!",
            likes_count=1,
            board_id=1),
        Card(message="You're doing great!!",
            likes_count=10,
            board_id=1),
    ])
    db.session.commit()


@pytest.fixture
def one_board(app):
    new_board = Board(title="Going outside daily",
                      owner="Jenny")

    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def four_boards(app):
    db.session.add_all([
        Board(title="vacation",
              owner="Jenny"),
        Board(title="travel",
              owner="Malik"),
        Board(title="333 - 22",
              owner="Esther"),
        Board(title="~Words~",
              owner="Brian"),
    ])
    db.session.commit()


@pytest.fixture
def mock_upload():
    with patch("app.routes.route_utilities.upload_to_s3") as mock:
        yield mock


@pytest.fixture
def mock_image_file():
    image = BytesIO(b"fake image data")
    image.name = "test_image.jpg"

    return image
