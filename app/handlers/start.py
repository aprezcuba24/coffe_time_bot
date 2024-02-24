from string import Template

from telegram import Update

START_TEXT = """
Hello "$name"!!
"""


def _content(update: Update):
    user = update.effective_user
    return dict(text=Template(START_TEXT).substitute(name=user.username))


def start_query(update: Update, *args):
    return update.effective_message.edit_text(**_content(update))


def start_command(update: Update, *args):
    return update.effective_message.reply_text(**_content(update))
