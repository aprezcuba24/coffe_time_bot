# import os
# import asyncio
# import logging
# from telegram.ext import ApplicationBuilder
# from app.config import configure, configure_handlers
# from app.utils.persistence import DynamodbPersistence

# TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# application = (
#     ApplicationBuilder()
#     .token(TELEGRAM_TOKEN)
#     .persistence(DynamodbPersistence())
#     .build()
# )

# loop = asyncio.get_event_loop()
# loop.create_task(configure(application.bot))

# configure_handlers(application)
# application.run_polling()

from app.main import main

main(
    {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/register-bot",
        "rawQueryString": "",
        "headers": {
            "content-length": "410",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-tls-version": "TLSv1.2",
            "x-amzn-trace-id": "Root=1-65d3f18f-65dc451a0f6a628a514847d7",
            "x-forwarded-proto": "https",
            "host": "l3nnfhvyiamvun7w6vcfehkllm0uprnd.cell-1-lambda-url.us-east-1.on.aws",
            "x-forwarded-port": "443",
            "content-type": "application/json",
            "x-forwarded-for": "91.108.6.117",
            "accept-encoding": "gzip, deflate",
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "l3nnfhvyiamvun7w6vcfehkllm0uprnd",
            "domainName": "l3nnfhvyiamvun7w6vcfehkllm0uprnd.cell-1-lambda-url.us-east-1.on.aws",
            "domainPrefix": "l3nnfhvyiamvun7w6vcfehkllm0uprnd",
            "http": {
                "method": "POST",
                "path": "/webhook",
                "protocol": "HTTP/1.1",
                "sourceIp": "91.108.6.117",
                "userAgent": None,
            },
            "requestId": "9def8f81-6e49-4dfa-8794-d893678288ec",
            "routeKey": "$default",
            "stage": "$default",
            "time": "20/Feb/2024:00:25:51 +0000",
            "timeEpoch": 1708388751606,
        },
        "body": '{"update_id":505130284,\n"message":{"message_id":19513,"from":{"id":982234904,"is_bot":false,"first_name":"Renier","last_name":"Ricardo Figueredo","username":"renierricardo","language_code":"en"},"chat":{"id":982234904,"first_name":"Renier","last_name":"Ricardo Figueredo","username":"renierricardo","type":"private"},"date":1708311064,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}',
        "isBase64Encoded": False,
    }
)
