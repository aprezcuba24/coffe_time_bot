import os

import boto3

region = os.environ.get("REGION")
dynamodb = boto3.resource("dynamodb", region_name=region)
PERSISTENCE_TABLE = os.environ.get("PERSISTENCE_TABLE")
RECORD_ID = "TELEGRAM_CHAT_DATA"


async def get_persistence_data():
    table = dynamodb.Table(PERSISTENCE_TABLE)
    Key = {"persistence_id": RECORD_ID}
    item = table.get_item(Key=Key)
    return item.get("Item", None)


async def save_data(data) -> None:
    table = dynamodb.Table(PERSISTENCE_TABLE)
    table.put_item(Item={**{"persistence_id": RECORD_ID}, **data})
