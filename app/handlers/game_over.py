from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, game_over_message


async def game_over_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    users = chat.game_over()
    if users is None:
        return await update.effective_message.reply_text(
            text="No hay ningún juego abierto."
        )
    await chat.save()
    await game_over_message(users, update)
