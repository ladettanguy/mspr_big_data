import json
from datetime import datetime
from typing import Dict, Any

from ..db import dao_mysql as mysql
from models.reservation import Reservation
from ..mspr import app
from flask import request


@app.route("/reserve", methods=["POST", "GET"])
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
    mysql.add_reservation(Reservation(0, parking.id_parking, utilisateur.id_utilisateur, datetime.now()))
    return {'success': True}
