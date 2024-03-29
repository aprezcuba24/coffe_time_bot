import telegram
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.handlers.add_user import add_user_command
from app.handlers.dice import dice_handler, no_play_dice_query, yes_play_dice_query
from app.handlers.game import play_command, play_no_query, play_yes_query
from app.handlers.game_over import game_over_command
from app.handlers.ranking import ranking_command
from app.handlers.remove_user import remove_user_command
from app.handlers.start import start_command, start_query
from app.handlers.who_are_left import who_are_left_command


async def configure(bot: telegram.Bot):
    common_commands = [
        ("play", "Comenzar nuevo juego."),
        ("add", "Adicionar usuario."),
        ("remove", "Eliminar usuario."),
        ("gameover", "Terminar partida"),
        ("wholeft", "Quiénes faltan por tirar."),
        ("ranking", "Ranking haciendo café"),
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


def configure_handlers(application: Application):
    application.add_handler(CommandHandler(command="start", callback=start_command))
    application.add_handler(CommandHandler(command="add", callback=add_user_command))
    application.add_handler(
        CommandHandler(command="remove", callback=remove_user_command)
    )
    application.add_handler(
        CommandHandler(command="wholeft", callback=who_are_left_command)
    )
    application.add_handler(CommandHandler(command="play", callback=play_command))
    application.add_handler(CommandHandler(command="ranking", callback=ranking_command))
    application.add_handler(
        CommandHandler(command="gameOver", callback=game_over_command)
    )
    application.add_handler(CallbackQueryHandler(start_query, pattern="start"))
    application.add_handler(
        CallbackQueryHandler(play_yes_query, pattern="game_yes_play")
    )
    application.add_handler(CallbackQueryHandler(play_no_query, pattern="game_no_play"))
    application.add_handler(
        CallbackQueryHandler(no_play_dice_query, pattern="dice_no_play")
    )
    application.add_handler(
        CallbackQueryHandler(yes_play_dice_query, pattern="dice_yes_play")
    )
    application.add_handler(
        MessageHandler(filters.Dice.DICE & filters.ChatType.GROUPS, dice_handler)
    )
