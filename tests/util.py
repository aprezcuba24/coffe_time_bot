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
    if "callback_query_data" in kwargs:
        update.callback_query.data = kwargs["callback_query_data"]
    if "user_id" in kwargs:
        update.effective_user.id = kwargs["user_id"]
    update.message.forward_from = (
        kwargs["forward_from"] if "forward_from" in kwargs else None
    )
    return update, context


async def _assert_save(data, context):
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1, data=data
    )


def _assert_chat_data(chat, data):
    print(data)
    print(chat.to_dict())
    assert chat.to_dict() == data


def _assert_reply_text(update, **kwargs):
    update.effective_message.reply_text.assert_called_once_with(**kwargs)


def _assert_edit_text(update, **kwargs):
    update.effective_message.edit_text.assert_called_once_with(**kwargs)


def _assert_send_photo(update, **kwargs):
    update.effective_chat.send_photo.assert_called_once_with(**kwargs)


async def get_chat(data, **kwargs):
    data = data if data else {}
    update, context = _load_params(**kwargs)

    async def get_chat_data():
        return {"1": data}

    context.application.persistence.get_chat_data = get_chat_data
    Chat._instance = None
    chat = await Chat.get_instance(update=update, context=context)

    async def assert_save(data):
        await _assert_save(data, context)

    def assert_chat_data(data):
        _assert_chat_data(chat, data)

    def assert_reply_text(**kwargs):
        _assert_reply_text(update, **kwargs)

    def assert_edit_text(**kwargs):
        _assert_edit_text(update, **kwargs)

    def assert_send_photo(**kwargs):
        _assert_send_photo(update, **kwargs)

    Chat._instance = None
    tester = Object()
    tester.chat = chat
    tester.assert_reply_text = assert_reply_text
    tester.update = update
    tester.context = context
    tester.assert_save = assert_save
    tester.assert_chat_data = assert_chat_data
    tester.assert_edit_text = assert_edit_text
    tester.assert_send_photo = assert_send_photo

    return tester
