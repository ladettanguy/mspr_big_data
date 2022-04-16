import datetime
from typing import Any, Dict

from flask_api import status
from flask import Flask, request
import json

import dao_mysql as mysql
from models import Reservation

app = Flask(__name__)


@app.route("/reserve", methods=["POST"])
def hello():
    json_request: str = request.json
    detail: Dict[str, Any] = json.loads(json_request)
    email = detail.get('email', None)
    id_parking = detail.get('id_parking', None)
    if not email or not id_parking:
        return status.HTTP_400_BAD_REQUEST
    parking = mysql.get_parking(id_parking)
    if not parking.id_parking:
        return status.HTTP_400_BAD_REQUEST
    utilisateur = mysql.get_utilisateur_from_email(email)
    if not utilisateur.id_utilisateur:
        return status.HTTP_400_BAD_REQUEST
    mysql.add_reservation(Reservation(0, parking.id_parking, utilisateur.id_utilisateur, datetime.datetime.now()))
    return {'success': True}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
