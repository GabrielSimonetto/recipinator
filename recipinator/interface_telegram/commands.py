from recipinator.domain import functionalities

from telegram import Bot, Update

from telegram.ext import CommandHandler


def iniciar(_: Bot, update: Update):
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
        update.message.reply_text(f"{result}")
        if i > 3:
            break


def favorite_recipe(_: Bot, update:Update):
    user_id = _get_user_id(update)
    recipe_id = update.message.text.split()[1]
    result_message = functionalities.set_favorite_recipe(user_id, recipe_id)

    update.message.reply_text(result_message)


def get_favorites(_: Bot, update:Update):
    user_id = _get_user_id(update)
    results = functionalities.get_favorites(user_id)

    for result in results:
        update.message.reply_text(f"{result}")

def _get_user(update: Update):
    return update["message"].from_user


def _get_user_id(update: Update):
    return _get_user(update)['id']


HANDLERS = [
    CommandHandler('iniciar', iniciar),
    CommandHandler('buscar', search_recipe),
    CommandHandler('favoritar', favorite_recipe),
    CommandHandler('meus_favoritos', get_favorites),
]