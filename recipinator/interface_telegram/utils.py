from telegram import Bot, Update

def _get_user(update: Update):
    return update["message"].from_user


def _get_user_id(update: Update):
    return _get_user(update)['id']

