import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler

from app.handlers.start import start_command, start_query

async def configure(bot: telegram.Bot):
    common_commands = []
    await bot.set_my_commands(
        commands=common_commands, scope=telegram.BotCommandScopeAllGroupChats()
    )
    await bot.set_my_commands([
        ("start", "Start to use the bot."),
    ] + common_commands)

def configure_handlers(application):
    application.add_handler(CommandHandler(command="start", callback=start_command))
    application.add_handler(CallbackQueryHandler(start_query, pattern="start"))
