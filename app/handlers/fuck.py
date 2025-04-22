from telegram import Update
from telegram.ext import ContextTypes
import random

from app.services.chat import Chat, user_not_active


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

    username = chat.active_username

    user_data = chat._users.get(username, {})
    user_has_lost = user_data.get("score", 0) > 0

    if user_has_lost:
        angry_emojis = ["💢", "🤬", "😡", "👿", "😤", "😠", "💥", "🔥", "👹", "👺"]
        angry_symbols = ["grrrr", "argh", "maldición", "!!!!", "@#$%&!", "¡¡¡$#@!!!", "ufff"]

        emojis = " ".join(random.sample(angry_emojis, k=min(3, len(angry_emojis))))
        symbol = random.choice(angry_symbols)

        return await update.effective_message.reply_text(
            text=f"{emojis} {symbol} {emojis}"
        )

    if not chat.has_open_game():
        return await update.effective_message.reply_text(
            text="No hay una partida abierta. Inicia una con /play primero."
        )

    if not chat.user_has_dice():
        return await update.effective_message.reply_text(
            text="Debes lanzar el dado primero."
        )

    # Check if the user has already used the fuck command in this game
    if user_data.get("fuck_active", False):
        return await update.effective_message.reply_text(
            text="¡No te pases! 🤡"
        )

    dice_value = chat.dice_value

    # Check if the dice value is 1 or 2
    if dice_value not in [1, 2]:
        return await update.effective_message.reply_text(
            text="Solo puedes usar este comando si sacaste 1 o 2 en el dado."
        )

    if username not in chat._users:
        chat._users[username] = {}

    chat._users[username]["fuck_active"] = True
    chat._users[username]["fuck_value"] = dice_value

    await chat.save()

    return await update.effective_message.reply_text(
        text=f"¡Preparado para joder! 😈 Cuando alguien saque {dice_value} o menos, recibirá tu maldición."
    )
