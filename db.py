import sqlite3
URL_DB = 'infogeneral.db'


def seleccion(sql) -> list:
    """ Ejecuta una consulta de selección sobre la base de datos """
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(sql).fetchall()
    except Exception:
        res = None
    return res


def accion(sql) -> int:
    """ Ejecuta una consulta de acción sobre la base de datos """
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(sql).rowcount
            if res != 0:
                con.commit()
    except Exception:
        res = 0
    return res
