import datetime
from typing import Any, Dict, Optional

import jwt
from flask import Flask, request
import json

import dao_mysql as mysql
from models import Utilisateur
from models.reservation import Reservation

app = Flask(__name__)
app.config['SECRET_KEY'] = "ABC"


@app.route('/')
def hello():
    return "Hello world !"


@app.route("/reserve", methods=["POST"])
def reserve():
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
        return "Method Not Allowed", 405
    dict_info: Dict[str, Optional[str]] = {
        'email': None,
        'pwd': None,
    }
    dict_info.update(request.json)
    if dict_info["email"] is None:
        return "Unauthorized", 401
    user: Utilisateur = mysql.get_utilisateur_from_email(dict_info["email"])
    if not user or user.pwd != dict_info['pwd']:
        return "Unauthorized", 401
    encoded_jwt = jwt.encode({"id": user.id_utilisateur, "utilisateur": user.email}, app.config['SECRET_KEY'], algorithm="HS256")
    return json.dumps({
        "success": True,
        "user": {"email": user.email},
        "jwt": encoded_jwt.decode('UTF-8'),
    })


@app.route("/register", methods=['POST'])
def register():
    if not request.method == "POST":
        return "Method Not Allowed", 405
    info = request.json
    email = info.get("email", None)
    pwd = info.get("pwd", None)
    if email is None or pwd is None:
        return "Bad request", 400
    user = mysql.get_utilisateur_from_email(email)
    if user.email is None:
        mysql.add_utilisateur(Utilisateur(email, pwd))
        return json.dumps({"success": True})
    else:
        return json.dumps({"error": "email already taken"}), 401


if __name__ == "__main__":
    app.run(host='0.0.0.0')
