from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, game_over_message, start_params


def get_buttons(user_id, message_id, value):
    YES_BUTTON = InlineKeyboardButton(
        text="Si",
        callback_data=f"dice_yes_play/{user_id}/{message_id}/{value}",
    )
    NO_BUTTON = InlineKeyboardButton(text="No", callback_data="dice_no_play")
    return [YES_BUTTON, NO_BUTTON]


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await update.effective_message.reply_text(
            text="Tu usuario no está activo. Adiciónalo primero."
        )
    if not chat.has_open_game():
        buttons = get_buttons(
            update.effective_user.id,
            update.effective_message.id,
            update.message.dice.value,
        )
        return await update.effective_message.reply_text(
            reply_markup=InlineKeyboardMarkup([buttons]),
            text="No hay una partida abierta. ¿Quiere abrir una?",
        )
    if chat.user_has_dice():
        return await update.effective_message.reply_text(
            text="Ya tiraste el dado.",
        )
    if not chat.user_can_dice():
        return await update.effective_message.reply_text(
            text="No puedes votar en esta ronda.",
        )
    chat.register_point()
    if chat.is_the_last_user():
        users = chat.game_over()
        await game_over_message(users, update)
    await chat.save()


def no_play_dice_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok")


async def yes_play_dice_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if chat.has_open_game():
        return
    [_, user_id, message_id, value] = update.callback_query.data.split("/")
    print(user_id, message_id, value)
    if update.effective_user.id != int(user_id):
        return
    users = chat.open_game()
    chat.register_point(int(message_id), int(value))
    await chat.save()
    return await update.effective_message.edit_text(**start_params(users))
