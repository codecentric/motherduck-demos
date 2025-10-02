from datetime import date

import duckdb

conn = duckdb.connect()
conn.execute("ATTACH DATABASE 'md:stackoverflow'")


def get_min_max():
    return conn.query("""
                      SELECT MIN(date (CreationDate)), MAX(date (CreationDate))
                      FROM stackoverflow.posts
                      """).fetchone()


def get_query(start_date: date, end_date: date):
    return f"""
        SELECT date (CreationDate) as day, count (*) as count
        FROM stackoverflow.posts
        WHERE date (CreationDate) BETWEEN '{start_date.strftime("%Y-%m-%d")}' AND '{end_date.strftime("%Y-%m-%d")}'
        GROUP BY day
        ORDER BY day
    """


def run_query(query):
    return conn.query(query).df()
