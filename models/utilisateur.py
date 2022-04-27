from typing import Any, Dict
from multipledispatch import dispatch


class Utilisateur:

    @dispatch(str, str)
    def __init__(self, email: str, pwd: str, id_utilisateur: int = -1):
        self.id_utilisateur = id_utilisateur
        self.email = email
        self.pwd = pwd

    @dispatch(dict)
    def __init__(self, dict_info: Dict[str, Any]):
        self.id_utilisateur = dict_info.get('id_utilisateur', -1)
        self.email = dict_info.get('email', None)
        self.pwd = dict_info.get('pwd', None)

    def __dict__(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'email': self.email,
            'pwd': self.pwd,
        }
