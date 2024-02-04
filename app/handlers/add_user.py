from telegram import Update
from telegram.ext import ContextTypes
from app.services.chat import add_user, get_chat_item


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


async def add_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if validate(update=update, context=context) is not None:
        return
    chat = update.effective_chat
    chat_data = await get_chat_item(update, context)
    for username in context.args:
        chat_data = add_user(username, chat_data)
    await context.application.persistence.update_chat_data(
        chat_id=chat.id, data=chat_data
    )
    return await update.effective_message.reply_text(
        text="Los usuarios fueron añadidos."
    )
