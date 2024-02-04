from telegram import Update
from telegram.ext import ContextTypes


def validate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return update.effective_message.reply_text(
            text="Debe pasar almenos un usuario."
        )
    bad_parameters = [item for item in context.args if not item.startswith("@")]
    if len(bad_parameters) > 0:
        return update.effective_message.reply_text(
            text=f"Estos valores no son usuarios válidos de telegram: {', '.join(bad_parameters)}"
        )


def add_user(username, chat_data):
    if "users" not in chat_data:
        chat_data["users"] = {}
    if username in chat_data["users"]:
        return chat_data
    chat_data["users"][username] = {}
    return chat_data


async def add_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if validate(update=update, context=context) is not None:
        return
    chat = update.effective_chat
    chats = await context.application.persistence.get_chat_data()
    chat_data = chats[chat.id]
    for username in context.args:
        chat_data = add_user(username, chat_data)
    await context.application.persistence.update_chat_data(
        chat_id=chat.id, data=chat_data
    )
    return await update.effective_message.reply_text(
        text="Los usuarios fueron añadidos."
    )
