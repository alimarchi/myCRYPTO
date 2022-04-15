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

    def get_euro_invested(self):
        con = sqlite3.connect("data/all_transactions.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT coin_from, SUM(quantity_from)
                    FROM transactions
                    WHERE coin_from = 'EUR'
                    GROUP BY coin_from
                    """
        )

        return cur.fetchone()

    def get_euro_to(self):
        con = sqlite3.connect("data/all_transactions.db")
        cur = con.cursor()

        cur.execute("""
                    SELECT coin_to, SUM(quantity_to)
                    FROM transactions
                    WHERE coin_to = 'EUR'
                    GROUP BY coin_to
                    """
        )

        return cur.fetchone()

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