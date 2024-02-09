from unittest.mock import AsyncMock

from app.services.chat import Chat


class Object(object):
    pass


def _load_params(**kwargs):
    update = AsyncMock()
    update.effective_chat.id = 1
    context = AsyncMock()
    if "username" in kwargs:
        update.effective_user.username = kwargs["username"]
    if "message_id" in kwargs:
        update.effective_message.id = kwargs["message_id"]
    if "message_value" in kwargs:
        update.message.dice.value = kwargs["message_value"]
    if "args" in kwargs:
        context.args = kwargs["args"]
    return update, context


async def _assert_save(chat, data, context):
    await chat.save()
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1, data=data
    )


def _assert_reply_text(update, **kwargs):
    update.effective_message.reply_text.assert_called_once_with(**kwargs)


async def get_chat(data, **kwargs):
    data = data if data else {}
    update, context = _load_params(**kwargs)

    async def get_chat_data():
        return {"1": data}

    context.application.persistence.get_chat_data = get_chat_data
    chat = await Chat.get_instance(update=update, context=context)

    assert_save = lambda data: (
        await _assert_save(chat, data, context) for _ in "_"
    ).__anext__()
    assert_reply_text = lambda **kwargs: (
        await _assert_reply_text(update, **kwargs) for _ in "_"
    ).__anext__()

    Chat._instance = None
    tester = Object()
    tester.chat = chat
    tester.assert_reply_text = assert_reply_text
    tester.update = update
    tester.context = context
    tester.assert_save = assert_save

    return tester
