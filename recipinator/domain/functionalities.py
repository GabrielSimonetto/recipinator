from telegram import Bot, Update

from recipinator.database import db

from recipinator.interface_telegram.recipinator import Recipe


def get_recipe(update: Update):
    title_recipe = update.message.text[16:]
    print(title_recipe)

    recipes = []
    for row in db.read_query("Select * from recipes"):
        recipes.append(Recipe(row[0],row[1],row[2]))

    results = []
    for recipe in recipes:
        if  title_recipe in recipe.name: 
            results.append(recipe)

    return results


def get_recipe_from_id(id):
    return Recipe(*db.get_recipe(id))


def set_favorite_recipe(user_id, recipe_id):
    db.insert_favorite_recipe(user_id, recipe_id)
    # unico jeito de nao dar seria se o recipe_id fosse invalido...
    # atualmente acho que isso quebra o codigo no banco de dados por causa das foreign keys
    # talvez seja importante pegar essa exceção aqui
    # mas ai da pra jogar com raises do db ate aqui, funciona melhor.
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

# tirar essa merda depois
def get_recipes_with_ingredient(ingredient_list=['sal', 'ovo']):
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
