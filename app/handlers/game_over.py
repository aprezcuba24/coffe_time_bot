from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import game_over, game_over_message


async def game_over_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await game_over(update, context)
    if users is None:
        return await update.effective_message.reply_text(
            text="No hay ningún juego abierto."
        )
    await game_over_message(users, update)
