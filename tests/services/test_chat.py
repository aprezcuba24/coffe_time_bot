from collections import defaultdict
from unittest.mock import AsyncMock

import pytest

from app.services.chat import Chat


async def get_chat(data, **kwargs):
    data = data if data else {}
    update = AsyncMock()
    update.effective_chat.id = 1
    if "username" in kwargs:
        update.effective_user.username = kwargs["username"]
    if "message_id" in kwargs:
        update.effective_message.id = kwargs["message_id"]
    if "message_value" in kwargs:
        update.message.dice.value = kwargs["message_value"]
    context = AsyncMock()

    async def get_chat_data():
        return {"1": data}

    context.application.persistence.get_chat_data = get_chat_data
    chat = await Chat.get_instance(update=update, context=context)

    async def assert_data(data):
        await chat.save()
        context.application.persistence.update_chat_data.assert_called_once_with(
            chat_id=1, data=data
        )

    Chat._instance = None
    return chat, assert_data


@pytest.mark.asyncio
async def test_add_user_it_there():
    chat, assert_data = await get_chat(
        {"users": {"@aaa": {}}, "active_users": ["@aaa"]}
    )
    chat.add_user("@bbb")
    await assert_data(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_remove_user():
    chat, assert_data = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        }
    )
    chat.remove_user("@bbb")
    await assert_data(
        {"users": {"@aaa": {}, "@bbb": {}}, "active_users": ["@aaa"], "cycles": []}
    )


@pytest.mark.asyncio
async def test_get_chat_item_not_chat():
    _, assert_data = await get_chat(defaultdict(dict, {}))
    await assert_data({"users": {}, "active_users": [], "cycles": []})


@pytest.mark.asyncio
async def test_get_chat_item_has_chat():
    _, assert_data = await get_chat(
        {"users": {"@aaaa": {}}, "active_users": ["@aaaa"], "cycles": []}
    )
    await assert_data(
        {
            "users": {"@aaaa": {}},
            "active_users": ["@aaaa"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_no_has_open_game():
    chat, _ = await get_chat({"cycles": []})
    assert not chat.has_open_game()


@pytest.mark.asyncio
async def test_has_open_game():
    chat, _ = await get_chat({"cycles": [{"users": [], "points": {}}]})
    assert chat.has_open_game()


@pytest.mark.asyncio
async def test_open_game(*args):
    chat, assert_data = await get_chat(
        {"active_users": ["@aaa", "@bbb"], "cycles": [{"users": [], "points": {}}]}
    )
    users = chat.open_game()
    assert users == ["@aaa", "@bbb"]
    await assert_data(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
        }
    )


@pytest.mark.asyncio
async def test_no_is_active_user():
    chat, _ = await get_chat({"active_users": ["@aaa", "@bbb"]}, username="ccc")
    assert not chat.is_active_user()


@pytest.mark.asyncio
async def test_is_active_user(*args):
    chat, _ = await get_chat({"active_users": ["@aaa", "@bbb"]}, username="aaa")
    assert chat.is_active_user()


@pytest.mark.asyncio
async def test_user_has_dice_no_has_open_game():
    chat, _ = await get_chat({})
    assert not chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_has_dice_no_has():
    chat, _ = await get_chat(
        {"active_users": ["@aaa", "@bbb"], "cycles": [{"points": {}, "users": []}]},
        username="aaa",
    )
    assert not chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_has_dice_has():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": {}, "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_can_dice_no():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert not chat.user_can_dice()


@pytest.mark.asyncio
async def test_user_can_dice():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
    )
    assert chat.user_can_dice()


@pytest.mark.asyncio
async def test_register_point_no_has_open_game():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        },
    )
    assert chat.register_point() is False


@pytest.mark.asyncio
async def test_register_point_user_has_dice():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert chat.register_point() is False


@pytest.mark.asyncio
async def test_register_point():
    chat, assert_data = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
        message_id=5555,
        message_value=5,
    )
    chat.register_point()
    await assert_data(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa"],
                    "points": {"@aaa": {"message_id": 5555, "value": 5}},
                }
            ],
        }
    )


@pytest.mark.asyncio
async def test_register_point_with_parameters():
    chat, assert_data = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
        message_id=5555,
        message_value=5,
    )
    chat.register_point(message_id=6666, value=6)
    await assert_data(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa"],
                    "points": {"@aaa": {"message_id": 6666, "value": 6}},
                }
            ],
        }
    )


@pytest.mark.asyncio
async def test_is_the_last_no():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
    )
    assert chat.is_the_last_user() is False


@pytest.mark.asyncio
async def test_is_the_last():
    chat, _ = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}, "@bbb": {}}}],
        },
    )
    assert chat.is_the_last_user()
