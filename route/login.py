import json

from ..db import dao_mysql as mysql
from flask import request
from mspr import app
from ..utils import jwt
from typing import Optional, Dict

from models import Utilisateur


@app.route("/login", methods=['POST', 'GET'])
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
    encoded_jwt = jwt.get_authentication_token(user)
    return json.dumps({
        "success": True,
        "user": {"email": user.email},
        "jwt": encoded_jwt.decode('UTF-8'),
    })
