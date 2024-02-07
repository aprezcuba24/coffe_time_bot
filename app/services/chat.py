from telegram import Update
from telegram.ext import ContextTypes


def start_params(users):
    return {"text": f"gogogogogogogogogogogogo \n {' '.join(users)}"}


def the_winner(user):
    return {"text": f"Tenemos un ganador {user}"}


def add_user(username, chat_data):
    if username in chat_data["users"] and username in chat_data["active_users"]:
        return chat_data
    chat_data["users"][username] = {}
    chat_data["active_users"] = chat_data["active_users"] + [username]
    return chat_data


def remove_user(username, chat_data):
    chat_data["active_users"] = [
        item for item in chat_data["active_users"] if item != username
    ]
    return chat_data


async def get_chat_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chats = await context.application.persistence.get_chat_data()
    chat_data = chats[str(chat.id)]
    if "users" not in chat_data:
        chat_data["users"] = {}
    if "active_users" not in chat_data:
        chat_data["active_users"] = []
    if "cycles" not in chat_data:
        chat_data["cycles"] = []
    return chat_data


async def has_open_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = await get_chat_item(update, context)
    return chat_data["cycles"] != []


async def open_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = await get_chat_item(update, context)
    active_users = chat_data["active_users"]
    chat_data["cycles"] = [
        {
            "users": active_users,
            "points": {},
        }
    ]
    await context.application.persistence.update_chat_data(
        chat_id=update.effective_chat.id, data=chat_data
    )
    return active_users


async def is_active_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = await get_chat_item(update, context)
    username = f"@{update.effective_user.username}"
    return username in chat_data["active_users"]


async def _user_has_dice(update: Update, cycle):
    users = [item for item in cycle["points"]]
    username = f"@{update.effective_user.username}"
    return username in users


async def _get_last_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_data = await get_chat_item(update, context)
    cycles = chat_data["cycles"]
    return cycles[len(cycles) - 1]


async def user_has_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_open_game(update, context):
        return False
    last_cycle = await _get_last_cycle(update, context)
    return await _user_has_dice(update, last_cycle)


async def user_can_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_cycle = await _get_last_cycle(update, context)
    username = f"@{update.effective_user.username}"
    return (
        not await _user_has_dice(update, last_cycle) and username in last_cycle["users"]
    )


async def register_point(
    update: Update, context: ContextTypes.DEFAULT_TYPE, message_id=None, value=None
):
    if not await has_open_game(update, context):
        return False
    chat_data = await get_chat_item(update, context)
    cycles = chat_data["cycles"]
    last_cycle = cycles[len(cycles) - 1]
    if await _user_has_dice(update, last_cycle):
        return False
    username = f"@{update.effective_user.username}"
    message_id = message_id if message_id is not None else update.effective_message.id
    value = value if value is not None else update.message.dice.value
    cycles[len(cycles) - 1]["points"][username] = {
        "message_id": message_id,
        "value": value,
    }
    chat_data["cycles"] = cycles
    await context.application.persistence.update_chat_data(
        chat_id=update.effective_chat.id, data=chat_data
    )


def _get_users_by_score(cycle):
    min_value = 7
    users = []
    for key, item in cycle["points"].items():
        if item["value"] < min_value:
            users = [(key, item)]
            min_value = item["value"]
        elif item["value"] == min_value:
            users.append((key, item))
    return [key for key, item in users]


async def is_the_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_cycle = await _get_last_cycle(update, context)
    print(last_cycle)
    return len(last_cycle["users"]) == len(last_cycle["points"])


async def game_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_open_game(update, context):
        return None
    chat_data = await get_chat_item(update, context)
    last_cycle = await _get_last_cycle(update, context)
    usernames = _get_users_by_score(last_cycle)
    if len(usernames) > 1:
        cycles = chat_data["cycles"]
        cycles.append(
            {
                "users": usernames,
                "points": {},
            }
        )
        chat_data["cycles"] = cycles
    else:
        user = usernames[0]
        if user not in chat_data["users"]:
            chat_data["users"][user] = {}
        score = chat_data["users"][user].get("score", 0)
        chat_data["users"][user]["score"] = score + 1
        chat_data["cycles"] = []
    await context.application.persistence.update_chat_data(
        chat_id=update.effective_chat.id, data=chat_data
    )
    return usernames
