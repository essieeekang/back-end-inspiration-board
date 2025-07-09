from sqlalchemy import desc
from flask import abort, make_response, request
from app.db import db
from uuid import uuid4
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
import boto3
import os


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

    return model.to_dict(), 201


def get_all_models(cls):
    query = db.select(cls)

    models = db.session.scalars(query)

    return [model.to_dict() for model in models]

def upload_to_s3(file):
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name = os.environ.get("AWS_REGION"),
        )

        s3_bucket = os.environ.get("S3_BUCKET_NAME")

        filename = secure_filename(file.filename)
        unique_filename = f"{uuid4()}_{filename}"

        result = s3_client.upload_fileobj(
            file,
            s3_bucket,
            unique_filename,
            ExtraArgs={"ACL": "public-read"},
        )

        return f"https://{s3_bucket}.s3.amazonaws.com/{unique_filename}"
    except ClientError as e:
        print(e)
        return None
