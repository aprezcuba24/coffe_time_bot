import asyncio
from datetime import datetime

from app.application import get_application
from app.services.chat import ChatItem, start_params

HOURS_DIFFERENCE = 5
application = get_application()


def main(event, *args, **kwargs):
    return asyncio.get_event_loop().run_until_complete(process_all(event))


async def process_all(event):
    chat_data = await application.persistence.get_chat_data()
    if not chat_data:
        return {"statusCode": 200, "body": "no_chat"}
    pivot_date = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
    print("event =>", event)
    for chat_id, chat_item in chat_data.items():
        await process_chat(pivot_date=pivot_date, chat_id=chat_id, chat_data=chat_item)
    return {"statusCode": 200, "body": "Success"}


async def process_chat(pivot_date, chat_id, chat_data):
    chat_item = ChatItem(chat_id=chat_id, persistence=application.persistence)
    chat_item.load_data(chat_data=chat_data)
    print(
        {
            "pivot_date": pivot_date.isoformat(),
            "last_play_date": chat_item.last_play_date.isoformat(),
            "chat_data": chat_data,
        }
    )
    if chat_item.last_play_date:
        delta = pivot_date.date() - chat_item.last_play_date.date()
        pivot_hour = pivot_date.hour - HOURS_DIFFERENCE
        last_play_date_hour = chat_item.last_play_date.hour - HOURS_DIFFERENCE
        print(
            {
                "pivot_hour": pivot_hour,
                "last_play_date_hour": last_play_date_hour,
                "delta.days": delta,
            }
        )
        # Open game if there is not a game today or it was in the morning.
        if delta.days > 0 or (pivot_hour > 12 and last_play_date_hour < 12):
            return await open_game_by_schedule(chat_id=chat_id, chat_item=chat_item)


async def open_game_by_schedule(chat_id, chat_item: ChatItem):
    users = chat_item.open_game()
    print(
        "open_game_by_schedule",
        {
            "chat_id": chat_id,
            "users": users,
        },
    )
    if len(users) > 0:
        await chat_item.save()
        return await send_message(chat_id, users)


async def send_message(chat_id, users):
    print("send_message =>", chat_id)
    return await application.bot.send_message(chat_id=chat_id, **start_params(users))
