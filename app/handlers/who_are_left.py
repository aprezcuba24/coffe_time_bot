from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat


async def who_are_left_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.has_open_game():
        return await update.effective_message.reply_text(text="No hay juego abierto")
    users = chat.who_are_left()
    if len(users) == 0:
        return await update.effective_message.reply_text(text="No Falta nadie")
    are_losing, value = chat.who_are_losing()
    return await update.effective_message.reply_text(
        text=f"Todavía faltan por tirar {' '.join(users)}\n"
        + f"Los perdedores hasta ahora, con {value} son: {' '.join(are_losing)}"
    )
