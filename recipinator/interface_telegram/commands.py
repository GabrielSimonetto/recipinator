from telegram import Bot, Update

from telegram.ext import CommandHandler

def iniciar(_: Bot, update: Update):
    message = ("Seja bem vindo ao Recipinator. \n"
              "Com este incrível bot sua vida e sua alimentação serão melhores!!\n"
              "Você pode enviar ingredientes que você gostaria de ter em uma receita" 
              "e iremos buscar a receita que abrange o máximo possível os ingredientes fornecidos.\n"
              "Você poderá também criar cardápios e favoritar as receitas que quiser.\n"
              "Com cardapios você conseguirá ver o valor nutricional das receitas adicionadas nele.")
    

    update.message.reply_text(message)


def search_recipe(_: Bot, update:Update):
    
    update.message.reply_text("Logo logo vou ter mandar receitas")

def favor(_: Bot, update:Update):

    update.message.reply_text("Logo logo vou favoritar suas receitas")



HANDLERS = [
    CommandHandler('iniciar', iniciar),
    CommandHandler('buscar', search_recipe),
    CommandHandler('favoritar', favor)
    ]