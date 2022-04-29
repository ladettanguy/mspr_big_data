import datetime

from models import Utilisateur, Parking


class Reservation:

    def __init__(self, id_parking: int, id_utilisateur: int, id_reservation: int = -1,
                 horraire_debut: datetime.datetime = datetime.datetime.now(), horraire_fin: datetime.date = None):
        self.id_reservation = id_reservation
        self.id_utilisateur = id_utilisateur
        self.id_parking = id_parking
        self.horraire_debut = horraire_debut
        self.horraire_fin = horraire_fin

    @staticmethod
    def from_user_parking(user: Utilisateur, parking: Parking):
        return Reservation(user.id_utilisateur, parking.id_parking)

    def __dict__(self):
        output_dict = {
            'id_reservation': self.id_reservation,
            'id_utilisateur': self.id_utilisateur,
            'id_parking': self.id_parking,
            'horraire_debut': self.horraire_debut,
            'horraire_fin': self.horraire_fin,
        }
        return output_dict
