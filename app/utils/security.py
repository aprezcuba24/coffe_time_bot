import os

from telegram import Update


def security(f):
    async def wrapper(update: Update, *args, **kwargs):
        admin_users = os.environ.get("ADMIN_USERS", "").split(",")
        username = update.effective_user.username
        if username not in admin_users:
            return await update.effective_message.reply_text(
                text="No tiene acceso a esta funcionalidad."
            )
        return await f(update, *args, **kwargs)

    return wrapper
