import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

TEXT = """
*Reglas del juego*

🚗 El que le toque hacer café busca el café si no hay.

🤺 El que haga café y deje los pozuelos con el café y el azúcar en el pantry, lo hace de nuevo.

🚰 Si no hay agua se hace de los bebederos, si no de los desechos líquidos del cuerpo.

📣 El que haga el café tiene que avisar en el canal.

*PD*
Las dudas verlas con @rpupo85 🤪
"""


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = os.environ.get("INFO_IMAGE_ID")
    return await update.message.reply_photo(
        photo=file_id, caption=TEXT, parse_mode=ParseMode.MARKDOWN
    )
