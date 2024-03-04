import os

from telegram.ext import Application

from app.utils.persistence import DynamodbPersistence


def get_application():
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    return (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .persistence(DynamodbPersistence())
        .build()
    )
