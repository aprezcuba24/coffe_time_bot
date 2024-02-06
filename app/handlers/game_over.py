from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import game_over


async def game_over_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await game_over(update, context)
    if users is None:
        return await update.effective_message.reply_text(
            text="No hay ningún juego abierto."
        )
    if len(users) == 1:
        return await update.effective_message.reply_text(
            text=f"Tenemos un ganador {users[0]}"
        )
    return await update.effective_message.reply_text(
        text=f"Desempate {' '.join(users)}"
    )
