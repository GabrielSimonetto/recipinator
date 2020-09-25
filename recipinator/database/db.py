import sqlite3

from recipinator import DB_PATH, RECIPE_TABLE_NAME
from recipinator.database.load_scraping_into_db import get_scraped_data

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


def _create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {RECIPE_TABLE_NAME}
            (title TEXT, 
            link TEXT)
    """)

def _insert_data():
    data_list = get_scraped_data()

    for recipe in data_list:
        c.execute(f"""
            INSERT INTO 
                {RECIPE_TABLE_NAME}
                (title, link)
            VALUES(
                ?, ?
            )""",
            (recipe['title'], recipe['link'])
        )
                # {recipe['title']}, {recipe['link']}
        conn.commit()

    c.close()
    conn.close()


def read_query(query):
    c.execute(query)
    return c.fetchall()


if __name__ == '__main__':
    _create_table()
    _insert_data()