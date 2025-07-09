from flask import  Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, upload_to_s3
from app.db import db
from app.models.card import Card
import requests

bp = Blueprint("cards_bp", __name__, url_prefix = "/cards")


@bp.get("")
def get_all_cards():
    query = db.select(Card)

    sort_param = request.args.get("sort")

    if sort_param == "likes":
        query = query.order_by(Card.likes_count.desc())

    if sort_param == "alphabetic":
        query = query.order_by(Card.message)

    cards = db.session.scalars(query)
    cards_response = [card.to_dict() for card in cards]

    return cards_response


@bp.get("/<id>")
def get_one_card(id):
    card = validate_model(Card, id)
    return card.to_dict()


@bp.delete("/<id>")
def delete_card(id):
    card = validate_model(Card, id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("")
def post_new_card():
    request_body = {
        "message": request.form.get("message"),
        "board_id": int(request.form.get("board_id"))
    }
    image_url = None

    if "image" in request.files:
        image_file = request.files['image']
        if image_file and image_file.filename != "":
            image_url = upload_to_s3(image_file)
            if image_url:
                request_body['image_url'] = image_url

    return create_model(Card, request_body)


@bp.patch("<id>/like", strict_slashes=False)
def increase_like_counts(id):
    card = validate_model(Card, id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict()
