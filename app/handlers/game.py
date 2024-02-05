from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.services.chat import has_open_game, open_game, start_params


YES_BUTTON = InlineKeyboardButton(text="Si", callback_data="game_yes_play")
NO_BUTTON = InlineKeyboardButton(text="No", callback_data="game_no_play")


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await has_open_game(update, context):
        return await update.effective_message.reply_text(
            reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
            text="Hay una partida abierta. ¿La quiere descartar?",
        )
    users = await open_game(update, context)
    return await update.effective_message.reply_text(**start_params(users))


async def play_yes_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await open_game(update, context)
    return await update.effective_message.edit_text(**start_params(users))


def play_no_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok el juego se mantiene activo.")
