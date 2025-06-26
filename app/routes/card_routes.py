from flask import  Blueprint, request, Response, abort, make_response
from .route_utilities import validate_model, create_model, get_all_models
from ..db import db
from app.models.card import Card
import os
import requests

bp = Blueprint("cards_bp", __name__, url_prefix = "/cards")


@bp.get("")
def get_all_cards():
    query = db.select(Card)

    sort_param = request.args.get("sort")

    if sort_param == "likes":
        query = query.order_by(Card.likes_count.desc())

    if sort_param == "alphabelic":
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
    request_body = request.get_json()
    return create_model(Card, request_body)


@bp.patch("<id>/like", strict_slashes=False)
def increase_like_counts(id):
    card = validate_model(Card, id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict()
