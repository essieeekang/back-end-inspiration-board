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


def test_post_new_card_with_image(client, one_board, mock_upload, mock_image_file):
    bucket = os.environ.get("S3_BUCKET_NAME")
    mock_upload.return_value = f"https://{bucket}.s3.amazonaws.com/test-image.jpg"

    post_response = client.post("/cards", data={
        "message": "Card with test image",
        "board_id": 1,
        "image": (mock_image_file, "test_image.jpg", "image/*"),
    },
    content_type="multipart/form-data")

    get_response = client.get("/cards")
    get_response_body = get_response.get_json()
    print(get_response_body[0])
    assert post_response.status_code == STATUS_CODE["CREATED"]
    assert len(get_response_body) == 1
    assert get_response_body[0]["image"] == f"https://{bucket}.s3.amazonaws.com/test-image.jpg"
    mock_upload.assert_called_once()


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
