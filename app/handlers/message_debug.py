import os

from telegram import Update
from telegram.ext import ContextTypes


async def message_debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username == "renierricardo":
        return await update.message.reply_text(text=update.message.to_json())
