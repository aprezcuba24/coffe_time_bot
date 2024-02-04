from telegram import Update
from telegram.ext import ContextTypes


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.dice)
    print(update.message.dice.value)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Dice")
