import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

from app.handlers.start import start_command, start_query
from app.handlers.add_user import add_user_command
from app.handlers.remove_user import remove_user_command
from app.handlers.dice import dice_handler
from app.handlers.game import play_command, play_yes_query, play_no_query


async def configure(bot: telegram.Bot):
    common_commands = [
        ("play", "Comenzar nuevo juego."),
        ("add", "Adicionar usuario."),
        ("remove", "Eliminar usuario."),
    ]
    await bot.set_my_commands(
        commands=common_commands, scope=telegram.BotCommandScopeAllGroupChats()
    )
    await bot.set_my_commands(
        [
            ("start", "Start to use the bot."),
        ]
        + common_commands
    )


def configure_handlers(application):
    application.add_handler(CommandHandler(command="start", callback=start_command))
    application.add_handler(CommandHandler(command="add", callback=add_user_command))
    application.add_handler(
        CommandHandler(command="remove", callback=remove_user_command)
    )
    application.add_handler(CommandHandler(command="play", callback=play_command))
    application.add_handler(CallbackQueryHandler(start_query, pattern="start"))
    application.add_handler(CallbackQueryHandler(play_yes_query, pattern="yes_play"))
    application.add_handler(CallbackQueryHandler(play_no_query, pattern="no_play"))
    application.add_handler(
        MessageHandler(filters.Dice.DICE & filters.ChatType.GROUP, dice_handler)
    )
