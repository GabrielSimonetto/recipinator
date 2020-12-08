import recipinator.database as db
from recipinator import RECIPE_TABLE_NAME

from recipinator.domain.classes import Recipe, Nutrient


def get_recipe(recipe_title):
    recipes = []
    for row in db.read_query(f"Select * from {RECIPE_TABLE_NAME}"):
        recipes.append(Recipe(row[0],row[1],row[2]))

    results = []
    for recipe in recipes:
        if recipe_title in recipe.name: 
            results.append(recipe)

    return results


def get_recipe_from_id(id):
    return Recipe(*db.get_recipe(id))


def set_favorite_recipe(user_id, recipe_id):
    db.insert_favorite_recipe(user_id, recipe_id)
    return "Receita favoritada com sucesso"


def get_favorites(user_id):
    favorites = db.get_favorites_from_user_id(user_id)

    recipes = []

    recipes = []
    for row in db.read_query("Select * from recipes"):
        recipes.append(Recipe(row[0],row[1],row[2]))

    favo = []
    for recipe in recipes:
        for favorite in favorites:
            if  favorite[1] == recipe.recipe_id:
                favo.append(recipe)

    return favo

def get_recipes_with_ingredient(ingredient_list):
    from collections import Counter

    ingredient_map = _map_ingredients_to_recipes(ingredient_list)
    ingredient_count = {i: len(j) for i,j in ingredient_map.items()}

    return (ingredient_map, ingredient_count)


def _map_ingredients_to_recipes(ingredient_list):
    from collections import defaultdict

    results = defaultdict(list)

    for ingredient_name in ingredient_list:
        recipe_ids = db.search_ingredient_on_recipes(ingredient_name)

        for i in recipe_ids:
            results[i].append(ingredient_name)

    return results


def search_nutrients_on(something):
    return db.search_nutrition(something)


def add_nutrient(nutrient_data, user_id):
    # Id will be corrected when inputing on BD
    nutrient = Nutrient(
        id = 42, 
        description = nutrient_data[0],
        energy_kcal = nutrient_data[1],
        carbohydrate_g = nutrient_data[2],
        protein_g = nutrient_data[3],
        lipid_g = nutrient_data[4],
        fiber_g = nutrient_data[5],
    )

    nutrient_id = db.insert_user_nutrient(user_id, **nutrient.__dict__)
    nutrient.id = nutrient_id

    return nutrient


def add_new_recipe(data, user_id):
    recipe_name = data[0]
    ingredients = data[1:]

    # Inputar a recipe no bd
    recipe_id = db.insert_user_recipe(user_id, recipe_name)
    
    # Inputar os ingredientes no banco
    db.insert_ingredients_table(recipe_id, ingredients)

    recipe = Recipe(recipe_id, recipe_name)
    return recipe

def get_ingredients_from_recipe(recipe_id):
    # ingredients = [('morango',), ('maçã',), ('laranja',), ('banana',), ('açucar',)]
    ingredients =  db.get_ingredients_from_recipe(recipe_id)
    ingredients = [i[0] for i in ingredients]
    return ingredients

