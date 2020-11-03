from telegram import Bot, Update

from recipinator.database import db

from recipinator.interface_telegram.recipinator import Recipe


def get_recipe(update: Update):
    title_recipe = update.message.text[8:]
    print(title_recipe)

    recipes = []
    for row in db.read_query("Select * from recipes"):
        recipes.append(Recipe(row[0],row[1],row[2]))

    results = []
    for recipe in recipes:
        if  title_recipe in recipe.name: 
            results.append(recipe)

    return results


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
