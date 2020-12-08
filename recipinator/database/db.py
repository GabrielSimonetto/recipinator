import sqlite3
import pandas as pd
from random import randrange

from recipinator import (
    DB_PATH,
    RECIPE_TABLE_NAME,
    INGREDIENTS_TABLE_NAME,
    FAVORITE_TABLE_NAME,
    USER_TABLE_NAME,
    NUTRIENTS_TABLE_NAME,
)
from recipinator.database.load_scraping_into_db import get_scraped_data
from recipinator.database.load_nutrient_information import get_nutrient_information

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()


def create_database():
    _create_table_recipes()
    _create_table_ingredients()
    _create_table_favorites()
    _create_table_users()

    _default_table_population()


# maybe generalize this later
# maybe always remove before creating seems better?
def _create_table_recipes():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {RECIPE_TABLE_NAME}
            (id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT,
            owner INTEGER)
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
    print("Populating recipes")
    recipes_data_list = get_scraped_data()
    _insert_data_recipes(recipes_data_list)

    print("Populating nutrients")
    nutrients_data = get_nutrient_information()
    nutrients_data['owner_id'] = None
    nutrients_data.to_sql(name=NUTRIENTS_TABLE_NAME,
                            con=conn,
                            if_exists='replace')

    c.close()
    conn.close()
    print("All is done!")

def _insert_data_recipes(data_list):
    def _insert_query(recipe):
        c.execute(f"""
            INSERT INTO 
                {RECIPE_TABLE_NAME}
                (title, link, owner)
            VALUES(
                ?, ?, ?
            )""",
            (recipe['title'], recipe['link'], None)
        )
        conn.commit()

    for recipe in data_list:
        # import ipdb; ipdb.set_trace()
        _insert_query(recipe)

        recipe_id = c.lastrowid

        print(
            f"Recipe id {recipe_id}\n"
            f"Title: {recipe['title']}\n"
        )

        insert_ingredients_table(recipe_id, recipe['ingredients'])


def insert_ingredients_table(recipe_id, ingredients):
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

def get_recipe(id):
    # TODO: Tratamento para receita com id de usuário.
    return read_query(
        f"""
        Select * from {RECIPE_TABLE_NAME} where id={id}
        """
    )[0]

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


def get_favorites_from_user_id(user_id):
    return read_query(f"""
        select * from {FAVORITE_TABLE_NAME} where user_id={user_id}
    """)

def search_ingredient_on_recipes(ingredient_name):
    """Returns a list of recipe_ids with the target ingredient"""

    ingredients = read_query(f"""
        select * from {INGREDIENTS_TABLE_NAME}
    """)

    # it was not needed to return a set,
    # I think i was already thinking of multi ingredient searches
    result = set()
    for recipe_id, ingredient in ingredients:
        if ingredient_name in ingredient:
            result.add(recipe_id)

    return result


def search_nutrition(ingredient_name):
    """Returns a list of rows on nutrition table that fit the ingredient name"""

    nutrients_df = pd.read_sql(f'select * from {NUTRIENTS_TABLE_NAME}', conn)
    mask_values_with_ingredient = nutrients_df['description'].apply(lambda el: ingredient_name in el)
    df = nutrients_df[mask_values_with_ingredient]
    dict_values = df[mask_values_with_ingredient].T.to_dict().values()
    return dict_values


def insert_user_nutrient(user_id,
                            description, 
                            energy_kcal, 
                            protein_g,
                            lipid_g,
                            carbohydrate_g,
                            fiber_g,
                            **kwargs):

    from random import randrange
    nutrient_id = randrange(600, 1000)

    c.execute(f"""
        INSERT INTO 
            {NUTRIENTS_TABLE_NAME}
            (
                id,
                description, 
                energy_kcal, 
                protein_g, 
                lipid_g, 
                carbohydrate_g, 
                fiber_g,
                owner_id
            )
        VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?
        )""",
        (
            nutrient_id,
            description, 
            energy_kcal, 
            protein_g, 
            lipid_g, 
            carbohydrate_g, 
            fiber_g,
            user_id
        )
    )
    conn.commit()

    return nutrient_id

def insert_user_recipe(user_id, recipe_name):
    c.execute(f"""
        INSERT INTO 
            {RECIPE_TABLE_NAME}
            (title, link, owner)
        VALUES(
            ?, ?, ?
        )""",
        (recipe_name, None, user_id)
    )
    conn.commit()

    recipe_id = c.lastrowid
    return recipe_id

def get_ingredients_from_recipe(recipe_id):
    return read_query(f"""
        select ingredient from {INGREDIENTS_TABLE_NAME} where recipe_id={recipe_id}
    """)

if __name__ == '__main__':
    create_database()