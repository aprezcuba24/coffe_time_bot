import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

TEXT = """
*Reglas del juego*

🚗 El que le toque hacer café busca el café si no hay.

🤺 El que haga café y deje los pozuelos con el café y el azúcar en el pantry, lo hace de nuevo.

🚰 Si no hay agua se hace de los bebederos, si no de los desechos líquidos del cuerpo.

*PD*
Las dudas verlas con @rpupo85 🤪
"""

INFO_IMAGE = "AgACAgEAAxkBAAJMSmYefIoFsoARV8KRanSpsM_mx2zeAAKyrDEbow3xRNB1ed6aYcwwAQADAgADcwADNAQ"


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_photo(
        photo=INFO_IMAGE, caption=TEXT, parse_mode=ParseMode.MARKDOWN
    )
