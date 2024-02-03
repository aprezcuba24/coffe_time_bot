import os
import asyncio
import logging
from telegram.ext import ApplicationBuilder
from app.config import configure, configure_handlers
from app.utils.persistence import DynamodbPersistence

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(TELEGRAM_TOKEN).persistence(DynamodbPersistence()).build()

loop = asyncio.get_event_loop()
loop.create_task(configure(application.bot))

configure_handlers(application)
application.run_polling()
