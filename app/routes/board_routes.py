from flask import Blueprint, request, Response, abort, make_response
from app.models.board import Board
from app.models.card import Card
from app.db import db
from .route_utilities import validate_model, create_model, get_all_models

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get("", strict_slashes=False)
def get_all_boards():
    return get_all_models(Board)


@bp.post("", strict_slashes=False)
def post_new_board():
    request_body = request.get_json()
    return create_model(Board, request_body)
