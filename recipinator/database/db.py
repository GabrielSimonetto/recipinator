import sqlite3

from recipinator import (
    DB_PATH,
    RECIPE_TABLE_NAME,
    FAVORITE_TABLE_NAME,
    USER_TABLE_NAME,
)
from recipinator.database.load_scraping_into_db import get_scraped_data

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()


# maybe generalize this later
def _create_table_recipes():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {RECIPE_TABLE_NAME}
            (id INTEGER PRIMARY KEY,
            title TEXT, 
            link TEXT)
    """)

def _create_table_favorites():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {FAVORITE_TABLE_NAME}
            (user_id INTEGER, 
            recipe_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES {USER_TABLE_NAME}(id),
            FOREIGN KEY(recipe_id) REFERENCES {RECIPE_TABLE_NAME}(id)          
            )
    """)

def _create_table_users():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME}
            (id INTEGER PRIMARY KEY)
    """)

def _insert_data_recipes(data_list):
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
        conn.commit()

# # Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

    c.close()
    conn.close()


def _default_table_population():
    recipes_data_list = get_scraped_data()
    _insert_data_recipes(recipes_data_list)


def read_query(query):
    c.execute(query)
    return c.fetchall()


if __name__ == '__main__':
    _create_table_recipes()
    _create_table_favorites()
    _create_table_users()

    _default_table_population()