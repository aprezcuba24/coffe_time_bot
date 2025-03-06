from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat


async def ignore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    message = "Ya fuiste ignorado. Que no te vea tomando café 😡"
    try:
        chat.ignore_user()
        await chat.save()
    except Exception as exc:
        message = exc.args[0]
    return await update.effective_message.reply_text(text=message)
