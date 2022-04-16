import datetime


class Reservation:

    def __init__(self, id_r: int, id_p: int, id_u: int, horraire_debut: datetime.date, horraire_fin: datetime.date = None):
        self.id_reservation = id_r
        self.id_utilisateur = id_u
        self.id_parking = id_p
        self.horraire_debut = horraire_debut
        self.horraire_fin = horraire_fin

    def __dict__(self):
        output_dict = {
            'id_reservation': self.id_reservation,
            'id_utilisateur': self.id_utilisateur,
            'id_parking': self.id_parking,
            'horraire_debut': self.horraire_debut,
        }
        if self.horraire_fin is not None:
            output_dict['horraire_fin'] = self.horraire_fin
        return output_dict
