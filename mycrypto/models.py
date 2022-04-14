import sqlite3


class DataHandle:

    def get_data(self):
        con = sqlite3.connect("data/all_transactions.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT date, time, coin_from, quantity_from,coin_to, quantity_to
                    FROM transactions
                    ORDER BY date
                    """
        )

        return cur.fetchall()

    def set_data(sel, params):
        con = sqlite3.connect("data/all_transactions.db")
        cur = con.cursor()

        cur.execute("""
        INSERT INTO transactions (date, time, coin_from, quantity_from, coin_to, quantity_to)
                    values (?,?,?,?,?,?)

        """, params)

        con.commit()
        con.close()

    def prueba(self):
        con = sqlite3.connect("data/prueba.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT DISTINCT moneda_to, SUM(cantidad_to)
                    FROM Prueba
                    GROUP BY moneda_to
                    """
        )

        return cur.fetchall()

    def prueba_2(self):
        con = sqlite3.connect("data/prueba.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT DISTINCT moneda_from, SUM(cantidad_from)
                    FROM Prueba
                    GROUP BY moneda_from
                    """
        )

        return cur.fetchall()

    def get_wallet(self):
        con = sqlite3.connect("data/all_transactions.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT coin_to, total_to - IFNULL(total_from, 0) AS difference
                    FROM(SELECT DISTINCT coin_to, SUM(quantity_to) AS total_to
                    FROM transactions
                    GROUP BY coin_to
                    HAVING coin_to <> 'EUR') AS A
                    LEFT JOIN (SELECT DISTINCT coin_from, SUM(quantity_from) AS total_from
                    FROM transactions
                    GROUP BY coin_from
                    HAVING coin_from<> 'EUR') AS B
                    ON A.coin_to = B.coin_from
                    """
        )

        return cur.fetchall()