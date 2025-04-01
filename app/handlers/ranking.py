from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.services.chat import Chat


def user_text(index, ranking):
    icons = ["🥇", "🥈", "🥉"]
    user, score = ranking
    icon = icons[index] if index < len(icons) else "🔸"
    username = user.replace("_", "")
    return f"{icon} {username} 👉 {score}"


async def ranking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = await Chat.get_instance(update, context)
    ranking = chat.ranking()
    if len(ranking) == 0:
        return await update.effective_message.reply_text(text="Todavía no hay ranking")
    list = [user_text(index, item) for index, item in enumerate(ranking)]
    print(list)
    return await update.effective_message.reply_text(
        text="\n".join(["*Ranking*"] + list),
        parse_mode=ParseMode.MARKDOWN,
    )
