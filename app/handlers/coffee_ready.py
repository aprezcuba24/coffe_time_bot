from telegram import Update
from telegram.ext import ContextTypes


async def coffee_ready_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.effective_message.reply_text(text="📣📣📣📣 YA ESTÁ EL CAFÉ.")
