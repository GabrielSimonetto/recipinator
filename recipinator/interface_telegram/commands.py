import random

from telegram import Bot, Update
from telegram.ext import CommandHandler

from recipinator.interface_telegram import utils
from recipinator.domain import functionalities, Recipe, Nutrient

MAX_RETURN_SIZE = 3


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
                '/ver_nutrientes <palavra>: retorna os nutrientes de <palavra>.\n'
                '/add_info_nutriente: adiciona um nutriente customizado.\n'
                '/add_receita: adiciona uma receita customizado.\n'
    )

    update.message.reply_text(message)


def search_recipe(_: Bot, update:Update):
    recipe_title = update.message.text[16:]
    results = functionalities.get_recipe(recipe_title)

    for result in results[:MAX_RETURN_SIZE]:
        update.message.reply_text(str(result))


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

    if len(ingredients) > 1:
        for recipe_id, _ in sorted(ingredient_count.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)[:MAX_RETURN_SIZE]:
            update.message.reply_text(f"Nessa receita encontrei: {ingredient_map[recipe_id]}\n\n"
                                        f"{functionalities.get_recipe_from_id(recipe_id)}")

    # se a gente tratar isso em outro lugar a gente pode até ja devolver a lista de 
    # receitas e vai ficar bem melhor, ai nao tem que acertar como cada iterador funca
    # inclusive ajuda a tratar o caso em que tu nao acha nada.
    elif len(ingredients) == 1:
        for recipe_id in [i for i in ingredient_count.keys()][:MAX_RETURN_SIZE]:
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
    def invalid_input_response():
        update.message.reply_text(
            "Insira as informações de nutrição segundo o exemplo: (explicações entre parenteses)\n"
            "\n"
            "/add_info_nutriente\n"
            "Amendoas (Nome do ingrediente)\n"
            "151 --- (kcal a cada 100g de ingrediente)\n"
            "15 ---- (gramas de carboidrato a cada 100g de ingrediente)\n"
            "4 ------ (gramas de proteína a cada 100g de ingrediente)\n"
            "15 ---- (gramas de gordura a cada 100g de ingrediente)\n"
            "4 ------ (gramas de fibra a cada 100g de ingrediente)\n"
        )

    def is_invalid_input(dados):
        if len(dados) != 6:
            return True

        # Valores após o nome devem ser inteiros.
        try:
            list(map(float, dados[1:]))
            return False
        except ValueError:
            return True

    raw = update.message.text[20:]
    dados = raw.split("\n")
    # removendo entradas vazias
    dados = [line for line in dados if line.strip() != ""]

    if is_invalid_input(dados):
        invalid_input_response()
        return

    user_id = utils._get_user_id(update)
    nutrient = functionalities.add_nutrient(dados, user_id)
    
    update.message.reply_text(f"Nutriente adicionado com sucesso!\n{nutrient}")

def add_recipe(_: Bot, update: Update):
    def invalid_input_response():
        update.message.reply_text(
            "Insira o titulo da receita na primeira linha, salte linhas para dividir os ingredientes.\n"
            "A versão atual ainda não suporta registro de modo de preparo.\n"
            "Explicações adicionais entre parenteses.\n"
            "\n"
            "/add_receita\n"
            "Yakisoba (Nome da receita)\n"
            "250g macarrao\n"
            "100g carne de porco\n"
            "100g carne de frango\n"
            "Meia cenoura\n"
            "Meio repolho\n"
            "Shoyu\n"
        )
    
    def is_invalid_input(dados):
        return True if len(dados) < 2 else False

    raw = update.message.text[13:]

    dados = raw.split("\n")
    # removendo entradas vazias
    dados = [line for line in dados if line.strip() != ""]

    if is_invalid_input(dados):
        invalid_input_response()
        return

    user_id = utils._get_user_id(update)
    recipe = functionalities.add_new_recipe(dados, user_id)
    
    update.message.reply_text(f"Receita adicionado com sucesso!\n{recipe}")


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
    CommandHandler('add_receita', add_recipe)
]