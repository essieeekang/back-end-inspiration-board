from app.models.card import Card
from app.db import db
import pytest
import os

STATUS_CODE = {"OK": 200, "CREATED": 201,"NO CONTENT": 204}

# GET route tests
def test_get_all_cards_no_sort(client, one_board, five_cards):
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert len(response_body) == 5
    assert response_body == [
        {
            "id": 1,
            "message": "Have a great day!",
            "likes": 0,
        },
        {
            "id": 2,
            "message": "Test msg!",
            "likes": 0,
        },
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 0,
        },
        {
            "id": 4,
            "message": "Eat a cookie!",
            "likes": 0,
        },
        {
            "id": 5,
            "message": "Take a break!",
            "likes": 0,
        },
    ]


def test_get_all_cards_with_likes_sort_param_desc(
        client, one_board, three_cards_with_likes):
    response = client.get("/cards?sort=likes")
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


def test_get_one_card(client, one_board, single_card):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert response_body == {
        "id": 1,
        "message": "Have a great day!",
        "likes": 0,
    }


# DELETE route test
def test_delete_card(client, one_board, five_cards):
    deletion_response = client.delete("/cards/2")
    get_response = client.get("/cards")
    get_response_body = get_response.get_json()

    assert deletion_response.status_code == STATUS_CODE["NO CONTENT"]
    assert len(get_response_body) == 4
    assert get_response_body == [
        {
            "id": 1,
            "message": "Have a great day!",
            "likes": 0,
        },
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 0,
        },
        {
            "id": 4,
            "message": "Eat a cookie!",
            "likes": 0,
        },
        {
            "id": 5,
            "message": "Take a break!",
            "likes": 0,
        },
    ]


# POST route test
def test_post_new_card(client, one_board):
    post_response = client.post("/cards", json={
        "message": "A new card!",
        "board_id": 1,
    })
    get_response = client.get("/cards")
    get_response_body = get_response.get_json()

    assert get_response.status_code == STATUS_CODE["OK"]
    assert len(get_response_body) == 1
    assert get_response_body == [{
        "id": 1,
        "message": "A new card!",
        "likes": 0,
    }]


# PATCH route test
def test_likes_count_increment(client, one_board, single_card):
    response = client.patch("/cards/1/like")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert response_body == {
        "id": 1,
        "message": "Have a great day!",
        "likes": 1,
    }
