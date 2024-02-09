from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat


async def validate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return await update.effective_message.reply_text(
            text="Debe pasar solo un usuario."
        )
    username = context.args[0]
    if not username.startswith("@"):
        return await update.effective_message.reply_text(
            text=f'Este valor "{username}" no es un usuario válido.'
        )


async def remove_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await validate(update=update, context=context) is not None:
        return
    chat = await Chat.get_instance(update, context)
    username = context.args[0]
    chat.remove_user(username)
    await chat.save()
    return await update.effective_message.reply_text(
        text=f"El usuario {username} fue eleminado."
    )
