from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat


async def images_by_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    images = chat.images_by_user()
    if len(images) == 0:
        return await update.effective_message.reply_text(text="Todavía no hay imágenes")
    for username, image in images:
        await update.effective_chat.send_photo(photo=image, caption=username)
