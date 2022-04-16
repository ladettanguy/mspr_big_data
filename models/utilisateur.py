from typing import Any, Dict
from multipledispatch import dispatch


class Utilisateur:

    @dispatch(int, str, str)
    def __init__(self, id_utilisateur: int, email: str, pwd: str):
        self.id_utilisateur = id_utilisateur
        self.email = email
        self.pwd = pwd

    @dispatch(Dict[str, Any])
    def __init__(self, dict_info: Dict[str, Any]):
        self.id_utilisateur = dict_info.get('id_utilisateur', None)
        self.email = dict_info.get('email', None)
        self.pwd = dict_info.get('pwd', None)

    def __dict__(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'email': self.email,
            'pwd': self.pwd,
        }
