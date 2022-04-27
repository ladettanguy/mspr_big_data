from typing import Any, Dict
from multipledispatch import dispatch


class Parking:

    @dispatch(str, str, str)
    def __init__(self, nom: str, ville: str, url_link: str, id_parking: int = -1):
        self.id_parking = id_parking
        self.nom = nom
        self.ville = ville
        self.lien_api_parking = url_link

    @dispatch(dict)
    def __init__(self, dict_info: Dict[str, Any]):
        self.id_parking = dict_info.get("id_parking", None)
        self.nom = dict_info.get("nom", None)
        self.ville = dict_info.get("ville", None)
        self.lien_api_parking = dict_info.get("lien_api_parking", None)

    def __dict__(self):
        return {
            'id_parking': self.id_parking,
            'nom': self.nom,
            'ville': self.ville,
            'lien_api_parking': self.lien_api_parking,
        }
