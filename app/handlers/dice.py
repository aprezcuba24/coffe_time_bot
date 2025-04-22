import time
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.services.chat import Chat, game_over_message, start_params, user_not_active


def get_buttons(user_id):
    YES_BUTTON = InlineKeyboardButton(
        text="Si",
        callback_data=f"dice_yes_play/{user_id}",
    )
    NO_BUTTON = InlineKeyboardButton(text="No", callback_data="dice_no_play")
    return [YES_BUTTON, NO_BUTTON]


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_from is not None:
        return await update.effective_message.reply_text(
            text="No se permite hacer forward.\nDebe lanzar el dado en el canal. 😡"
        )
    chat = await Chat.get_instance(update, context)
    if not chat.is_active_user():
        return await user_not_active(update)
    if not chat.has_open_game():
        buttons = get_buttons(update.effective_user.id)
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

    current_username = chat.active_username
    current_dice_value = chat.dice_value

    fuck_users = []
    for username, user_data in chat._users.items():
        if (username != current_username and
            user_data.get("fuck_active", False) and
            current_dice_value <= user_data.get("fuck_value", 6)):
            fuck_users.append(username)

    if fuck_users:
        emojis = ["💩", "🖕", "🤡", "👹", "💀", "😈", "🤬", "🔪", "👺", "🤮"]
        emoji = random.choice(emojis)

        reactions = [
            "¡Te jodieron!",
            "¡Alguien te ha dado una maldición!",
            "¡Qué mal número, te han jodido!",
            "¡Alguien está feliz de verte sufrir!",
            "¡Mala suerte, te han maldecido!"
        ]
        reaction = random.choice(reactions)

        for username in fuck_users:
            chat._users[username]["fuck_active"] = False

        await update.effective_message.reply_text(
            text=f"{reaction} {emoji} {' '.join(fuck_users)} está disfrutando tu infortunio."
        )

    if chat.is_the_last_user():
        users = chat.game_over()
        time.sleep(5)
        await game_over_message(users, update)
    await chat.save()


def no_play_dice_query(update: Update, *args):
    return update.effective_message.edit_text(text="Ok")


async def yes_play_dice_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if chat.has_open_game():
        return
    [_, user_id] = update.callback_query.data.split("/")
    if update.effective_user.id != int(user_id):
        return
    users = chat.open_game()
    await chat.save()
    return await update.effective_message.edit_text(**start_params(users))
