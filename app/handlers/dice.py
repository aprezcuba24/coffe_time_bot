from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import (
    has_open_game,
    is_active_user,
    open_game,
    register_point,
    start_params,
    user_can_dice,
    user_has_dice,
)


def get_buttons(message_id, value):
    YES_BUTTON = InlineKeyboardButton(
        text="Si",
        callback_data=f"dice_yes_play/{message_id}/{value}",
    )
    NO_BUTTON = InlineKeyboardButton(text="No", callback_data="dice_no_play")
    return [YES_BUTTON, NO_BUTTON]


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_active_user(update, context):
        return await update.effective_message.reply_text(
            text="Tu usuario no está activo. Adiciónalo primero."
        )
    if not await has_open_game(update, context):
        buttons = get_buttons(update.effective_message.id, update.message.dice.value)
        return await update.effective_message.reply_text(
            reply_markup=InlineKeyboardMarkup([buttons]),
            text="No hay una partida abierta. ¿Quiere abrir una?",
        )
    if await user_has_dice(update, context):
        return await update.effective_message.reply_text(
            text="Ya tiraste el dado.",
        )
    if not await user_can_dice(update, context):
        return await update.effective_message.reply_text(
            text="No puedes votar en esta ronda.",
        )
    await register_point(update, context)


def no_play_dice_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok")


async def yes_play_dice_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await has_open_game(update, context):
        return
    parts = update.callback_query.data.split("/")
    await register_point(update, context, int(parts[1]), int(parts[2]))
    users = await open_game(update, context)
    return update.effective_message.edit_text(**start_params(users))
