from datetime import datetime, date

import duckdb

conn = duckdb.connect()
conn.execute("ATTACH DATABASE 'md:stackoverflow'")

# initialize cache for the last 1 year
cache_cutoff = "2022-03-05"
cache_query = f"""
    CREATE TABLE IF NOT EXISTS posts_local_cache AS (
        SELECT date (CreationDate) as day, count (*) as count
        FROM stackoverflow.posts
        WHERE day BETWEEN '{cache_cutoff}' AND '2023-03-05'
        GROUP BY day)
"""
print(f"initialize cache with {cache_query}")
conn.query(cache_query)


def get_min_max():
    return conn.query("""
                      SELECT MIN(date (CreationDate)), MAX(date (CreationDate))
                      FROM stackoverflow.posts
                      """).fetchone()


def get_query(start_date: date, end_date: date):
    if start_date > datetime.fromisoformat(cache_cutoff).date():
        return f"""
            SELECT day, count
            FROM posts_local_cache
            WHERE day BETWEEN '{start_date.strftime("%Y-%m-%d")}' AND '{end_date.strftime("%Y-%m-%d")}'
            ORDER BY day"""
    else:
        return f"""
            SELECT date (CreationDate) as day, count (*) as count
            FROM stackoverflow.posts
            WHERE date (CreationDate) BETWEEN '{start_date.strftime("%Y-%m-%d")}' AND '{end_date.strftime("%Y-%m-%d")}'
            GROUP BY day
            ORDER BY day
        """


def run_query(query):
    return conn.query(query).df()
