from app.models.card import Card
from app.db import db
import pytest
import os
from unittest.mock import patch

STATUS_CODE = {"OK": 200, "CREATED": 201,"NO CONTENT": 204}

# GET route tests
@patch('app.models.card.randint', return_value=0)  # Always return first color
def test_get_all_cards_no_sort(mock_randint, client, one_board, five_cards):
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert len(response_body) == 5
    assert response_body == [
        {
            "id": 1,
            "message": "Have a great day!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 2,
            "message": "Test msg!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 4,
            "message": "Eat a cookie!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 5,
            "message": "Take a break!",
            "likes": 0,
            "color": "#db96b9",
        },
    ]


@patch("app.models.card.randint", return_value=0)  # Always return first color
def test_get_all_cards_with_likes_sort_param_desc(
        mock_randint, client, one_board, three_cards_with_likes):
    response = client.get("/cards?sort=likes")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 10,
            "color": "#db96b9",
        },
        {
            "id": 1,
            "message": "Have a great day!",
            "likes": 3,
            "color": "#db96b9",
        },
        {
            "id": 2,
            "message": "Test msg!",
            "likes": 1,
            "color": "#db96b9",
        },
    ]


@patch("app.models.card.randint", return_value=0)  # Always return first color
def test_get_one_card(mock_randint, client, one_board, single_card):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert response_body == {
        "id": 1,
        "message": "Have a great day!",
        "likes": 0,
        "color": "#db96b9",
    }


# DELETE route test
@patch("app.models.card.randint", return_value=0)  # Always return first color
def test_delete_card(mock_randint, client, one_board, five_cards):
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
            "color": "#db96b9",
        },
        {
            "id": 3,
            "message": "You're doing great!!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 4,
            "message": "Eat a cookie!",
            "likes": 0,
            "color": "#db96b9",
        },
        {
            "id": 5,
            "message": "Take a break!",
            "likes": 0,
            "color": "#db96b9",
        },
    ]


# POST route test
@patch("app.models.card.randint", return_value=0)  # Always return first color
def test_post_new_card(mock_randint, client, one_board):
    client.post("/cards", json={
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
        "color": "#db96b9",
    }]


# PATCH route test
@patch("app.models.card.randint", return_value=0)  # Always return first color
def test_likes_count_increment(mock_randint, client, one_board, single_card):
    response = client.patch("/cards/1/like")
    response_body = response.get_json()

    assert response.status_code == STATUS_CODE["OK"]
    assert response_body == {
        "id": 1,
        "message": "Have a great day!",
        "likes": 1,
        "color": "#db96b9",
    }
