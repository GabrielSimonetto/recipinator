import json

from telegram import Bot, Update
from telegram.ext import CommandHandler

from recipinator.domain import functionalities
from recipinator.interface_telegram import utils
from recipinator.interface_telegram.recipinator import Recipe
from recipinator.interface_telegram.nutrients import Nutrient


def start(_: Bot, update: Update):
    message = ("Seja bem vindo ao Recipinator. \n\n"
              "Com este incrível bot sua vida e sua alimentação serão melhores!!\n\n"
              "Você pode enviar ingredientes que você gostaria de ter em uma receita" 
              " e iremos buscar a receita que abrange o máximo possível os ingredientes fornecidos.\n\n"
              "Você poderá também criar cardápios e favoritar as receitas que quiser.\n\n"
              "Com cardapios você conseguirá ver o valor nutricional das receitas adicionadas nele.\n\n"
              "Chame /help para ver como usar os comandos.")

    update.message.reply_text(message)


def _help(_: Bot, update: Update):
    message = ('/start: mensagem de boas vindas.\n'
                '/buscar_receita <palavra>: retorna receitas com <palavra> no titulo.\n'
                '/favoritar <id>: favorita a receita do respectivo id.\n'
                '/meus_favoritos: retorna suas receitas favoritas.\n'
                '/buscar_ingredientes <ingr1> <ingr2>: busca um ou multiplos ingredientes na receita.\n'
                '/ver_nutrientes <palavra>: retorna os nutrientes de <palavra>.\n')

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
    # TODO: retornar um "boh nao achei nada" se nao achar nada.

    raw = update.message.text
    ingredients = raw[21:]
    ingredients.strip()
    ingredients = ingredients.split(' ')

    if ingredients == ['']:
        update.message.reply_text("Por favor insira um alimento para ser buscado")
        return

    ingredient_map, ingredient_count = functionalities.get_recipes_with_ingredient(ingredients)

    RETURN_SIZE = 3
    if len(ingredients) > 1:
        for recipe_id, _ in sorted(ingredient_count.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)[:RETURN_SIZE]:
            update.message.reply_text(f"Nessa receita encontrei: {ingredient_map[recipe_id]}\n\n"
                                        f"{functionalities.get_recipe_from_id(recipe_id)}")

    # se a gente tratar isso em outro lugar a gente pode até ja devolver a lista de 
    # receitas e vai ficar bem melhor, ai nao tem que acertar como cada iterador funca
    # inclusive ajuda a tratar o caso em que tu nao acha nada.
    elif len(ingredients) == 1:
        for recipe_id in [i for i in ingredient_count.keys()][:RETURN_SIZE]:
            update.message.reply_text(f"{functionalities.get_recipe_from_id(recipe_id)}")

    else:
        update.message.reply_text(f"Algo deu errado, voce enviou {raw}, parece certo?")

    
def check_nutrients(_: Bot, update: Update):
    raw = update.message.text
    recipe_or_ingredient = raw[16:]
    recipe_or_ingredient.strip()

    if recipe_or_ingredient == '':
        update.message.reply_text("Por favor insira um alimento para ser buscado")
        return

    result_list = functionalities.search_nutrients_on(recipe_or_ingredient)

    for food in result_list:
        nutrient = Nutrient(**food)
        update.message.reply_text(str(nutrient))

def add_nutrient_information(_: Bot, update: Update):
    raw = update.message.text[20:]
    dados = raw.split("\n")
    
    nutrient = Nutrient(1, dados[1], float(dados[2]), float(dados[3]), float(dados[4]), float(dados[5]), float(dados[6]))

    print(nutrient.__repr__)

    # Não consegui fazer com que envia-se para o usuario.
    
    # update.message.reply_text(json.dumps(nutrient.__repr__))

HANDLERS = [
    # TODO retornar uma mensagem de erro se o comando nao bater com nada.
    CommandHandler('start', start),
    CommandHandler('help', _help),
    CommandHandler('buscar_receita', search_recipe),
    CommandHandler('favoritar', favorite_recipe),
    CommandHandler('meus_favoritos', get_favorites),
    CommandHandler('buscar_ingredientes', search_ingredient),
    CommandHandler('ver_nutrientes', check_nutrients),
    CommandHandler('add_info_nutriente', add_nutrient_information),
]