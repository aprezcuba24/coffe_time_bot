from telegram import Update
from telegram.ext import ContextTypes

from app.services.chat import Chat
from app.utils.security import security

PHOTO_POSITION = 3


@security
async def images_by_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    images = chat.images_by_user()
    if len(images) == 0:
        return await update.effective_message.reply_text(text="Todavía no hay imágenes")
    for username, image in images:
        await update.effective_chat.send_photo(photo=image, caption=username)


@security
async def image_of_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    if len(context.args) != 1:
        return await update.effective_message.reply_text(text="Debe pasar un usuario.")
    image = chat.image_of_user(context.args[0])
    if image is None:
        return await update.effective_message.reply_text(text="No hay imagen")
    await update.effective_message.reply_photo(photo=image)


@security
async def upload_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    username = update.effective_message.caption
    if not chat.has_username(username):
        return await update.effective_message.reply_text(text="El usuario no existe.")
    photoSize = update.effective_message.photo[PHOTO_POSITION]
    chat.update_image_of_user(username, photoSize.file_id)
    await chat.save()
    return await update.effective_message.reply_text(text="Hecho.")
