from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, start_params, user_not_active

YES_BUTTON = InlineKeyboardButton(text="Si", callback_data="game_yes_play")
NO_BUTTON = InlineKeyboardButton(text="No", callback_data="game_no_play")


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)
    if chat.has_open_game():
        return await update.effective_message.reply_text(
            reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
            text="Hay una partida abierta. ¿La quiere descartar?",
        )
    users = chat.open_game()
    await chat.save()
    return await update.effective_message.reply_text(**start_params(users))


async def play_yes_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    users = chat.open_game()
    await chat.save()
    return await update.effective_message.edit_text(**start_params(users))


def play_no_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok el juego se mantiene activo.")
