from telegram import Update
from telegram.ext import ContextTypes
from app.services.chat import remove_user, get_chat_item


def validate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return update.effective_message.reply_text(text="Debe pasar solo un usuario.")
    username = context.args[0]
    if not username.startswith("@"):
        return update.effective_message.reply_text(
            text=f'Este valor "{username}" no es un usuario válido.'
        )


async def remove_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if validate(update=update, context=context) is not None:
        return
    chat = update.effective_chat
    chat_data = await get_chat_item(update, context)
    username = context.args[0]
    print(chat_data)
    chat_data = remove_user(username, chat_data)
    print(chat_data)
    await context.application.persistence.update_chat_data(
        chat_id=chat.id, data=chat_data
    )
    return await update.effective_message.reply_text(
        text=f"El usuario {username} fue eleminado."
    )
