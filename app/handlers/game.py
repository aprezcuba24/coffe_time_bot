from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, start_params

YES_BUTTON = InlineKeyboardButton(text="Si", callback_data="game_yes_play")
NO_BUTTON = InlineKeyboardButton(text="No", callback_data="game_no_play")


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if chat.has_open_game():
        return await update.effective_message.reply_text(
            reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
            text="Hay una partida abierta. ¿La quiere descartar?",
        )
    users = chat.open_game()
    if len(users) == 0:
        return await update.effective_message.reply_text(
            text="Primero debe registrar usuarios."
        )
    await chat.save()
    return await update.effective_message.reply_text(**start_params(users))


async def play_yes_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    users = chat.open_game()
    await chat.save()
    return await update.effective_message.edit_text(**start_params(users))


def play_no_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok el juego se mantiene activo.")
