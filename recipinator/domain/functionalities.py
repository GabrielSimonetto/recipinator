from telegram import Bot, Update

from recipinator.database import db

from recipinator.interface_telegram.recipinator import Recipe

def get_recipe(update: Update):
    title_recipe = update.message.text[8:]
    print(title_recipe)
    recipes = []

    for row in db.read_query("Select * from recipes"):
        recipes.append(Recipe(row[0],row[1],row[2]))
        print(row)

    results = []

    for recipe in recipes:
        if  title_recipe in recipe.name: 
            results.append(recipe)

    return results

