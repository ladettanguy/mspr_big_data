import jwt

from mspr import app
from models import Utilisateur


def get_authentication_token(user: Utilisateur):
    return jwt.encode(
            {
                "id": user.id_utilisateur,
                "utilisateur": user.email,
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        ).decode("UTF-8")
