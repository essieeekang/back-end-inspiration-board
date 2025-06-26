from app.models.board import Board
from app.db import db
import pytest

STATUS_CODE = {"OK": 200, "NO CONTENT": 204}


# GET route tests
def test_get_all_boards_no_sort(client, four_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert len(response_body) == 4
    assert response_body == [
        {
            "id": 1,
            "title": "vacation",
            "owner": "Jenny",
        },
        {
            "id": 2,
            "title": "travel",
            "owner": "Malik",
        },
        {
            "id": 3,
            "title": "333 - 22",
            "owner": "Esther",
        },
        {
            "id": 4,
            "title": "~Words~",
            "owner": "Brian",
        },
    ]


def test_get_cards_by_board(client, one_board, three_cards_with_likes):
    response = client.get("/boards/1/cards?sort=likes")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 10,
        },
        {
            "id": 1,
            "message": "Have a great day!",
            "likes": 3,
        },
        {
            "id": 2,
            "message": "Test msg!",
            "likes": 1,
        },
    ]


# DELETE route test (for current DELETE route; will likely change in future)
def test_delete_board(client, four_boards):
    deletion_response = client.delete("/boards/4")
    get_response = client.get("/boards")
    get_response_body = get_response.get_json()

    assert deletion_response.status_code == STATUS_CODE["NO CONTENT"]
    assert len(get_response_body) == 3
    assert get_response_body == [
        {
            "id": 1,
            "title": "vacation",
            "owner": "Jenny",
        },
        {
            "id": 2,
            "title": "travel",
            "owner": "Malik",
        },
        {
            "id": 3,
            "title": "333 - 22",
            "owner": "Esther",
        },
    ]


# POST route test
def test_post_new_board(client):
    post_response = client.post("/boards", json={
        "title": "A Test Board",
        "owner": "Ada L",
    })
    get_response = client.get("/boards")
    get_response_body = get_response.get_json()

    assert get_response.status_code == STATUS_CODE["OK"]
    assert len(get_response_body) == 1
    assert get_response_body == [{
        "id": 1,
        "title": "A Test Board",
        "owner": "Ada L",
    }]
