from sqlalchemy import desc
from flask import abort, make_response, request
from app.db import db

def validate_model(cls, model_id):
    """Returns validated model.

    Function validates model_id and returns a model if the model exists in the
    database.
    """
    try:
        model_id = int(model_id)
    except ValueError:
        message = {"error": f"{cls.__name__} id ({model_id}) is invalid."}
        abort(make_response(message, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        message = {"error": f"{cls.__name__} id ({model_id}) not found."}
        abort(make_response(message, 404))

    return model


def create_model(cls, model_data):
    try:
        model = cls.from_dict(model_data)
    except KeyError:
        response = {"error": "Invalid model data."}
        abort(make_response(response, 400))

    db.session.add(model)
    db.session.commit()

    return {f"{model}": model.to_dict()}, 201


def get_all_models(cls):
    query = db.select(cls)

    models = db.session.scalars(query)

    return [model.to_dict() for model in models]

# def get_models_with_filters(cls):
