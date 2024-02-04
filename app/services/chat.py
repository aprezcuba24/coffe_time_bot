from telegram import Update
from telegram.ext import ContextTypes


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
        chat_data["c"] = []
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
    return (active_users, chat_data)
