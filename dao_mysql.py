import datetime
import os

import pymysql

from typing import Dict, Callable
from pymysql.connections import Connection
from multipledispatch import dispatch
from models import Utilisateur, Parking, Reservation
from pymysql.cursors import DictCursor

__config_db = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'passwd': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'cursorclass': DictCursor,
}


def get_connection() -> Connection:
    return pymysql.connect(**__config_db)


def get_dict_from_row(result_sql: list) -> Dict[int, Dict]:
    output_dict: Dict[int, Dict] = {}
    for index, result_dict in enumerate(result_sql):
        output_dict[index] = result_dict
    return output_dict


def make_request(func: Callable):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            return func(connection, cursor)


def add_utilisateur(user: Utilisateur):
    def a(conn, cur):
        cur.execute("INSERT INTO utilisateur VALUE (%s, %s, %s);", (user.id_utilisateur, user.email, user.pwd))
        conn.commit()

    make_request(a)


def add_parking(p: Parking):
    def a(conn, cur):
        cur.execute('INSERT INTO parking VALUE (%s, %s, %s, %s);',
                    (p.id_parking, p.nom, p.ville, p.lien_api_parking))
        conn.commit()

    make_request(a)


@dispatch(Utilisateur, Parking)
def add_reservation(user: Utilisateur, p: Parking):
    def a(conn, cur):
        cur.execute("SELECT MAX(id_parking) as count from reservation;")
        id_reservation = cur.fetchall()[0]['count'] + 1
        cur.execute("INSERT INTO reservation (id_reservation, horaire_debut, id_parking, id_utilisateur)"
                    "VALUE (%s, %s, %s, %s);",
                    (id_reservation, datetime.datetime.now(), p.id_parking, user.id_utilisateur))
        conn.commit()

    make_request(a)


@dispatch(Reservation)
def add_reservation(r: Reservation):
    def a(conn, cur):
        cur.execute("SELECT MAX(id_parking) as count from reservation;")
        id_reservation = cur.fetchall()[0]['count'] + 1
        cur.execute("INSERT INTO reservation (id_reservation, horaire_debut, id_parking, id_utilisateur) "
                    "VALUE (%s, %s, %s, %s);",
                    (id_reservation, datetime.datetime.now(), r.id_parking, r.id_utilisateur))
        conn.commit()

    make_request(a)


def get_parking_in_ville(nom_ville: str):
    def a(_, cur):
        cur.execute("SELECT * FROM parking WHERE ville=%s;", [nom_ville])
        return get_dict_from_row(cur.fetchall())
    list_to_return = []
    result = make_request(a)
    for _, dict_info in result.items():
        list_to_return.append(Parking(dict_info))
    return list_to_return


def get_parking(id_parking: int):
    def a(_, cur):
        cur.execute("SELECT * FROM parking WHERE id_parking=%s", [id_parking])
        return get_dict_from_row(cur.fetchall())
    result = make_request(a)
    return Parking(result[0])


def get_utilisateur_from_email(email: str):
    def a(_, cur):
        cur.execute("SELECT * FROM utilisateur WHERE email=%s", [email])
        return get_dict_from_row(cur.fetchall())
    result = make_request(a)
    return Utilisateur(result[0])


add_utilisateur(Utilisateur(0, 's@gmail.com', 'hauzehrazhjk'))
add_parking(Parking(0, 'parking1', 'email', "https//niquetamere.com/"))
