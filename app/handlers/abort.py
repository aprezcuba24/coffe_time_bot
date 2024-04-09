from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, user_not_active

YES_BUTTON = InlineKeyboardButton(text="Si", callback_data="abort_yes")
NO_BUTTON = InlineKeyboardButton(text="No", callback_data="abort_no")


async def abort_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)
    if not chat.has_open_game():
        return await update.effective_message.reply_text(
            text="No hay partida abierta.",
        )
    return await update.effective_message.reply_text(
        reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
        text="¿Está seguro, quiere abortar el juego?",
    )


async def abort_yes_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    chat.abort()
    await chat.save()
    return await update.effective_message.edit_text(
        text=f"El juego fue abortado por {chat.active_username}"
    )


def abort_no_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok el juego se mantiene activo.")
