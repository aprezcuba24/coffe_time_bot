from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat


async def validate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.effective_message.reply_text(
            text="Debe pasar almenos un usuario."
        )
    bad_parameters = [item for item in context.args if not item.startswith("@")]
    if len(bad_parameters) > 0:
        return await update.effective_message.reply_text(
            text=f"Estos valores no son usuarios válidos de telegram: {', '.join(bad_parameters)}"
        )


async def add_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await validate(update=update, context=context) is not None:
        return
    chat = await Chat.get_instance(update, context)
    for username in context.args:
        chat.add_user(username)
    await chat.save()
    return await update.effective_message.reply_text(
        text="Los usuarios fueron añadidos."
    )
