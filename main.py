import datetime
import http
from typing import Any, Dict

import jwt
from flask import Flask, request
import json

import dao_mysql as mysql
from models import Utilisateur
from models.reservation import Reservation

app = Flask(__name__)


@app.route("/reserve", methods=["POST"])
def hello():
    json_request: str = request.json
    detail: Dict[str, Any] = json.loads(json_request)
    email = detail.get('email', None)
    id_parking = detail.get('id_parking', None)
    if not email or not id_parking:
        return
    parking = mysql.get_parking(id_parking)
    if not parking.id_parking:
        return
    utilisateur = mysql.get_utilisateur_from_email(email)
    if not utilisateur.id_utilisateur:
        return
    mysql.add_reservation(Reservation(0, parking.id_parking, utilisateur.id_utilisateur, datetime.datetime.now()))
    return {'success': True}


@app.route("/login", methods=['POST'])
def login():
    if not request.method == 'POST':
        return http.HTTPStatus.METHOD_NOT_ALLOWED
    dict_info: Dict[str, str] = {
        'email': "",
        'pwd': "",
    }
    dict_info.update(json.loads(request.get_json()))
    if not dict_info["email"]:
        return http.HTTPStatus.BAD_REQUEST
    user: Utilisateur = mysql.get_utilisateur_from_email(dict_info["email"])
    if user.pwd == hash(dict_info['pwd']):
        return http.HTTPStatus.UNAUTHORIZED
    encoded_jwt = jwt.encode({"id": user.id_utilisateur, "utilisateur": user.email}, "secret", algorithm="HS256")
    print(encoded_jwt)
    return {
        "success": True,
        "user": {"email": None},
        "jwt": encoded_jwt,
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0')
