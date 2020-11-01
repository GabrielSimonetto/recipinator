import sqlite3

from recipinator import (
    DB_PATH,
    RECIPE_TABLE_NAME,
    INGREDIENTS_TABLE_NAME,
    FAVORITE_TABLE_NAME,
    USER_TABLE_NAME,
)
from recipinator.database.load_scraping_into_db import get_scraped_data

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()


# maybe generalize this later
# maybe always remove before creating seems better?
def _create_table_recipes():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {RECIPE_TABLE_NAME}
            (id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT)
    """)

def _create_table_ingredients():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {INGREDIENTS_TABLE_NAME}
            (recipe_id INTEGER,
            ingredient TEXT,
            FOREIGN KEY(recipe_id) REFERENCES {RECIPE_TABLE_NAME}(id)
            )
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

def _default_table_population():
    recipes_data_list = get_scraped_data()
    _insert_data_recipes(recipes_data_list)

def _insert_data_recipes(data_list):
    def _insert_query(recipe):
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

    for recipe in data_list:
        _insert_query(recipe)

        recipe_id = c.lastrowid

        print(
            f"Recipe id {recipe_id}\n"
            f"Title: {recipe['title']}\n"
        )

        _insert_ingredients_table(recipe_id, recipe['ingredients'])

    c.close()
    conn.close()

def _insert_ingredients_table(recipe_id, ingredients):
    for ingredient in ingredients:
        c.execute(f"""
            INSERT INTO
                {INGREDIENTS_TABLE_NAME}
                (recipe_id, ingredient)
            VALUES(
                ?, ?
            )""",
            (recipe_id, ingredient)
        )
        conn.commit()

def read_query(query):
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    return result

def insert_favorite_recipe(user_id, recipe_id):
    c.execute(f"""
        INSERT INTO 
            {FAVORITE_TABLE_NAME}
            (user_id, recipe_id)
        VALUES(
            ?, ?
        )""",
        (user_id, recipe_id)
    )
    conn.commit()

    c.close()
    conn.close()

def get_favorites_from_user_id(user_id):
    return read_query(f"""
        select * from {FAVORITE_TABLE_NAME} where user_id={user_id}
    """)

def search_ingredient(ingredient_name):
    """Returns a list of recipe_ids with the target ingredient"""

    ingredients = read_query(f"""
        select * from {INGREDIENTS_TABLE_NAME}
    """)

    result = set()
    for recipe_id, ingredient in ingredients:
        if ingredient_name in ingredient:
            result.add(recipe_id)

    return result

if __name__ == '__main__':
    _create_table_recipes()
    _create_table_ingredients()
    _create_table_favorites()
    _create_table_users()

    _default_table_population()