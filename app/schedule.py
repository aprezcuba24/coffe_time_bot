import json
from datetime import datetime

from app.handlers.game import open_game_by_schedule
from app.services.chat import ChatItem
from app.services.persistence_data import get_persistence_data

HOURS_DIFFERENCE = -5


async def main(event, *args, **kwargs):
    data = await get_persistence_data()
    if not data:
        return {"statusCode": 200, "body": "no_chat"}
    chat_data = json.loads(data["chat_data"])
    pivot_date = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
    for chat_id, chat_item in chat_data.items():
        await process_chat(pivot_date=pivot_date, chat_id=chat_id, chat_data=chat_item)
    return {"statusCode": 200, "body": "Success"}


async def process_chat(pivot_date, chat_id, chat_data):
    chat_item = ChatItem(chat_id=chat_id)
    chat_item.load_data(chat_data=chat_data)
    if "last_play_date" in chat_data and chat_data["last_play_date"] is not None:
        last_play_date = datetime.fromisoformat(chat_data["last_play_date"])
        delta = pivot_date - last_play_date
        pivot_hour = pivot_date.hour - HOURS_DIFFERENCE
        last_play_date_hour = last_play_date.hour - HOURS_DIFFERENCE
        if delta.days == 0 and (
            (pivot_hour < 12 and last_play_date_hour < 12)
            or (pivot_hour > 12 and last_play_date_hour > 12)
        ):
            return
    return await open_game_by_schedule(chat_id=chat_id, chat_item=chat_item)
