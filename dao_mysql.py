import datetime
import os

import pymysql

from typing import Dict, Callable
from pymysql.connections import Connection
from multipledispatch import dispatch
from models import Utilisateur, Parking
from models.reservation import Reservation
from pymysql.cursors import DictCursor

__config_db = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'passwd': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'cursorclass': DictCursor,
}


def _get_connection() -> Connection:
    return pymysql.connect(**__config_db)


def _get_new_id(connection: Connection):
    with connection.cursor() as cursor:
        cursor.execute('SELECT LAST_INSERT_ID() as id')
        return cursor.fetchall()[0]['id']


def _get_dict_from_row(result_sql: list) -> Dict[int, Dict]:
    output_dict: Dict[int, Dict] = {}
    for index, result_dict in enumerate(result_sql):
        output_dict[index] = result_dict
    return output_dict


def _make_request(connection: Connection, func: Callable):
    with connection.cursor() as cursor:
        return func(connection, cursor)


def add_utilisateur(user: Utilisateur):
    def a(conn, cur):
        cur.execute('INSERT INTO utilisateur (email, pwd) VALUE (%s, %s);', (user.email, user.pwd))
        conn.commit()

    with _get_connection() as connection:
        _make_request(connection, a)
        user.id_utilisateur = _get_new_id(connection)


def add_parking(p: Parking):
    def a(conn, cur):
        cur.execute('INSERT INTO parking (nom, ville, lien_api_parking) VALUE (%s, %s, %s);',
                    (p.nom, p.ville, p.lien_api_parking))
        conn.commit()

    with _get_connection() as connection:
        _make_request(connection, a)
        p.id_parking = _get_new_id(connection)


@dispatch(Utilisateur, Parking)
def add_reservation(user: Utilisateur, parking: Parking) -> Reservation:
    r = Reservation.from_user_parking(user, parking)
    add_reservation(r)
    return r


@dispatch(Reservation)
def add_reservation(r: Reservation):
    def a(conn, cur):
        cur.execute("INSERT INTO reservation (horaire_debut, id_parking, id_utilisateur) "
                    "VALUE (%s, %s, %s);",
                    (r.horraire_debut, r.id_parking, r.id_utilisateur))
        conn.commit()

    with _get_connection() as connection:
        _make_request(connection, a)
        r.id_reservation = _get_new_id(connection)


def get_parking_in_ville(nom_ville: str):
    def a(_, cur):
        cur.execute("SELECT * FROM parking WHERE ville=%s;", [nom_ville])
        return _get_dict_from_row(cur.fetchall())
    list_to_return = []
    with _get_connection() as connection:
        result = _make_request(connection, a)
        for _, dict_info in result.items():
            list_to_return.append(Parking(dict_info))
    return list_to_return


def get_parking(id_parking: int):
    def a(_, cur):
        cur.execute("SELECT * FROM parking WHERE id_parking=%s", [id_parking])
        return _get_dict_from_row(cur.fetchall())

    with _get_connection() as connection:
        result = _make_request(connection, a)
        return Parking(result[0])


def get_utilisateur_from_email(email: str):
    def a(_, cur):
        cur.execute("SELECT * FROM utilisateur WHERE email=%s", [email])
        return _get_dict_from_row(cur.fetchall())

    with _get_connection() as connection:
        result = _make_request(connection, a)
        return Utilisateur(result[0])
