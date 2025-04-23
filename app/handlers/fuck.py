from telegram import Update
from telegram.ext import ContextTypes
import random

from app.services.chat import Chat, user_not_active
from app.services.fuck_service import FuckService


async def fuck_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command that takes the value of the dice and sends a reaction and emoji
    to the next person that gets a number like yours or less.
    If the user has lost the game, it just sends random angry emojis.
    Only users with dice values of 1 or 2 can use this command.
    """
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)

    if not chat.has_open_game():
        return await update.effective_message.reply_text(
            text="No hay una partida abierta. Inicia una con /play primero."
        )
    if not chat.user_has_dice():
        return await update.effective_message.reply_text(
            text="Debes lanzar el dado primero."
        )
    if chat.has_fuck():
        return await update.effective_message.reply_text(text="¡No te pases! 🤡")

    dice_value = chat.dice_value

    if not FuckService.is_valid_dice_value(dice_value):
        return await update.effective_message.reply_text(
            text="Vamos, no llores tanto, ganate el privilegio de usar el comando, tira un 1 o un 2."
        )
    chat.register_fuck(dice_value)
    await chat.save()
    return await update.effective_message.reply_text(
        text=f"¡Preparado para joder! 😈 Cuando alguien saque {dice_value} o menos, recibirá tu maldición."
    )
