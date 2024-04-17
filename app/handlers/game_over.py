from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, game_over_message, user_not_active


async def game_over_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)
    if not chat.has_open_game():
        return await update.effective_message.reply_text(
            text="No hay ningún juego abierto."
        )
    users = chat.game_over()
    if users is None:
        return await update.effective_message.reply_text(
            text="Todavía no se ha jugado."
        )
    await chat.save()
    await game_over_message(users, update)
