from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, game_over_message, user_not_active


async def game_over_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)
    users = chat.game_over()
    await chat.save()
    if users is None or len(users) == 0:
        return await update.effective_message.reply_text(
            text="No hay ningún juego abierto o no se llegó a jugar."
        )
    await game_over_message(users, update)
