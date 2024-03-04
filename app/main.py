import asyncio
import json
import traceback

from telegram import Bot, Update
from telegram.ext import Application

from app.config import configure, configure_handlers

from app.application import get_application


def main(event, *args, **kwargs):
    print(event)
    application = get_application()
    routes = {
        "/webhook": webhook,
        "/register-bot": register_bot,
    }
    func = routes.get(event["rawPath"], not_found)
    return asyncio.get_event_loop().run_until_complete(func(event, application))


async def not_found(event, *args):
    return {
        "statusCode": 404,
        "body": "Not found",
    }


async def webhook(event, application: Application):
    configure_handlers(application)
    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return {"statusCode": 200, "body": "Success"}

    except Exception as exc:
        print("webhook =>", "Exception")
        print(exc)
        print(traceback.format_exc())
        return {"statusCode": 200, "body": "Failure"}


async def register_bot(event, application: Application):
    url = f"https://{event['requestContext']['domainName']}/webhook"
    bot: Bot = application.bot
    await bot.set_webhook(url)
    bot_user = await bot.get_me()
    body = {"webhook_url": url, "bot": bot_user.to_dict(), "input": event}
    await configure(bot=bot)
    return {"statusCode": 200, "body": json.dumps(body)}
