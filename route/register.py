from flask import request
import json
from ..db import dao_mysql as mysql
from mspr import app
from models import Utilisateur
from utils import jwt


@app.route("/register", methods=['POST', 'GET'])
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
        new_user = Utilisateur(email, pwd)
        mysql.add_utilisateur(new_user)
        encoded_jwt = jwt.get_authentication_token(new_user)
        return json.dumps({"success": True, "user": {"email": user.email}, "jwt": encoded_jwt})
    else:
        return json.dumps({"error": "email already taken"}), 401
