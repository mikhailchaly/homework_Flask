from typing import Type

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, Advert
from schema import CreateAdvert, UpdateAdvert

app = Flask('app')

class HttpError(Exception):
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema: Type[CreateAdvert] | Type[UpdateAdvert], json_data: dict):
    try:
        model = schema(**json_data)
        validated_data = model.model_dump(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated_data


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    http_response = jsonify({"status": "error", "description": er.error_message})
    http_response.status_code = er.status_code
    return http_response

def get_advert(session: Session, advert_id: int):
    advert = session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, "advert not found")
    return advert


class AdvertView(MethodView):
    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(session, advert_id)
            return jsonify(
                {
                    "id": advert.id,
                    "title": advert.title,
                    "description": advert.description,
                    "owner": advert.owner,
                    "creation_time": advert.creation_time.isoformat(),
                }
            )
    def post(self):
        json_data = validate(CreateAdvert, request.json)
        with Session() as session:
            advert = Advert(**json_data)
            session.add(advert)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'advert alredy exists')
            return jsonify({'status': "succes", "id": advert.id})

    def patch(self, advert_id: int):
        json_data = validate(UpdateAdvert, request.json)
        with Session() as session:
            advert = get_advert(session, advert_id)

            for field, value in json_data.items():
                setattr(advert, field, value)
            session.add(advert)
            session.commit()
            return jsonify({"status": "success", "id": advert.id})

    def delete(self, advert_id):
        with Session() as session:
            advert = get_advert(session, advert_id)
            session.delete(advert)
            session.commit()
            return jsonify({"status": "success", "id": advert_id})

advert_view = AdvertView.as_view("advert")

app.add_url_rule(
    "/advert/<int:advert_id>", view_func=advert_view, methods=["GET", "PATCH", "DELETE"]
)

app.add_url_rule("/advert/", view_func=advert_view, methods=["POST"])


if __name__ == '__main__':
    app.run()