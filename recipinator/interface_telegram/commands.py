from recipinator.domain import functionalities

from recipinator.interface_telegram import utils

from recipinator.database import db

from telegram import Bot, Update

from telegram.ext import CommandHandler

from recipinator.interface_telegram.recipinator import Recipe

from recipinator.interface_telegram.nutrients import Nutrient



def start(_: Bot, update: Update):
    message = ("Seja bem vindo ao Recipinator. \n\n"
              "Com este incrível bot sua vida e sua alimentação serão melhores!!\n\n"
              "Você pode enviar ingredientes que você gostaria de ter em uma receita" 
              " e iremos buscar a receita que abrange o máximo possível os ingredientes fornecidos.\n\n"
              "Você poderá também criar cardápios e favoritar as receitas que quiser.\n\n"
              "Com cardapios você conseguirá ver o valor nutricional das receitas adicionadas nele.")

    update.message.reply_text(message)


def search_recipe(_: Bot, update:Update):
    results = functionalities.get_recipe(update)
    
    for i, result in enumerate(results):
        update.message.reply_text(str(result))
        if i > 3:
            break


def favorite_recipe(_: Bot, update:Update):
    user_id = utils._get_user_id(update)
    recipe_id = update.message.text.split()[1]
    result_message = functionalities.set_favorite_recipe(user_id, recipe_id)

    update.message.reply_text(result_message)


def get_favorites(_: Bot, update:Update):
    user_id = utils._get_user_id(update)
    results = functionalities.get_favorites(user_id)

    
    for recipe in results:
        print((recipe))
        update.message.reply_text(str(recipe))

def search_ingredient(_: Bot, update: Update):
    ingredient = update.message.text
    ingredient = ingredient[13:]
    ingredient = ingredient.strip()

    if "," in ingredient:
        list_ingredient = ingredient.split(",")
        recipes_list = functionalities.get_recipes_with_ingredient(list_ingredient)
        print("recipes_list")
        for recipe in recipes_list:
             update.message.reply_text(recipe.link)
        
    elif len(ingredient) > 1:
        recipes_list = functionalities.get_recipes_with_ingredient(ingredient)
        for recipe in recipes_list:
            update.message.reply_text(recipe.link)
    else:
        update.message.reply_text("Por favor, escreva os ingredientes semparados por virgulas")

def check_nutrients(_: Bot, update: Update):
    recipe = update.message.text
    recipe = recipe[16:]
    recipe.strip()

    list_recipes = db.search_ingredient_nutrition(recipe)

    print(list_recipes)

    for i in list_recipes:
        from pprint import pprint
        pprint(i)
        recipe_nut = Nutrient(i["id"], i["description"], i["energy_kcal"], i["protein_g"], i["lipid_g"], i["carbohydrate_g"], i["fiber_g"])
        update.message.reply_text(str(recipe_nut))

HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('buscar', search_recipe),
    CommandHandler('favoritar', favorite_recipe),
    CommandHandler('ingredientes', search_ingredient),
    CommandHandler('meus_favoritos', get_favorites),
    CommandHandler('ver_nutrientes', check_nutrients),
]