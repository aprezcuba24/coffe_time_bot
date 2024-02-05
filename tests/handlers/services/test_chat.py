import pytest
from collections import defaultdict
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.chat import (
    add_user,
    remove_user,
    get_chat_item,
    has_open_game,
    open_game,
    is_active_user,
    user_has_dice,
    user_can_dice,
    register_point,
)


def test_add_user_it_there():
    chat_data_param = {"users": {"@aaa": {}}, "active_users": ["@aaa"]}
    chat_data = add_user("@aaa", chat_data_param)
    assert chat_data == chat_data_param


def test_add_user():
    chat_data_param = {"users": {"@aaa": {}}, "active_users": ["@aaa"]}
    chat_data = add_user("@bbb", chat_data_param)
    assert chat_data == {
        "users": {"@aaa": {}, "@bbb": {}},
        "active_users": ["@aaa", "@bbb"],
    }


def test_remove_user():
    chat_data_param = {
        "users": {"@aaa": {}, "@bbb": {}},
        "active_users": ["@aaa", "@bbb"],
    }
    chat_data = remove_user("@bbb", chat_data_param)
    assert chat_data == {"users": {"@aaa": {}, "@bbb": {}}, "active_users": ["@aaa"]}


@pytest.mark.asyncio
async def test_get_chat_item_not_chat():
    update = MagicMock()
    context = MagicMock()
    update.effective_chat.id = 1

    async def get_chat_data():
        return defaultdict(dict, {})

    context.application.persistence.get_chat_data = get_chat_data
    chat_data = await get_chat_item(update, context)
    assert chat_data == {"users": {}, "active_users": [], "cycles": []}


@pytest.mark.asyncio
async def test_get_chat_item_has_chat():
    update = MagicMock()
    context = MagicMock()
    update.effective_chat.id = 1

    async def get_chat_data():
        return {"1": {"users": {"@aaaa": {}}, "active_users": ["@aaaa"], "cycles": []}}

    context.application.persistence.get_chat_data = get_chat_data
    chat_data = await get_chat_item(update, context)
    assert chat_data == {
        "users": {"@aaaa": {}},
        "active_users": ["@aaaa"],
        "cycles": [],
    }


@pytest.mark.asyncio
@patch("app.services.chat.get_chat_item", return_value={"cycles": []})
async def test_no_has_open_game(*args):
    assert not await has_open_game(None, None)


@pytest.mark.asyncio
@patch("app.services.chat.get_chat_item", return_value={"cycles": [{}]})
async def test_has_open_game(*args):
    assert await has_open_game(None, None)


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={"active_users": ["@aaa", "@bbb"], "cycles": [{}]},
)
async def test_open_game(*args):
    update = AsyncMock()
    update.effective_chat.id = 1
    context = AsyncMock()
    assert await open_game(update, context) == ["@aaa", "@bbb"]
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
        },
    )


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={"active_users": ["@aaa", "@bbb"]},
)
async def test_no_is_active_user(*args):
    update = AsyncMock()
    update.effective_user.username = "ccc"
    assert not await is_active_user(update, None)


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={"active_users": ["@aaa", "@bbb"]},
)
async def test_is_active_user(*args):
    update = AsyncMock()
    update.effective_user.username = "aaa"
    assert await is_active_user(update, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=False)
async def test_user_has_dice_no_has_open_game(*args):
    assert not await user_has_dice(None, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={"active_users": ["@aaa", "@bbb"], "cycles": [{}, {"points": {}}]},
)
async def test_user_has_dice_no_has(*args):
    update = AsyncMock()
    update.effective_user.username = "aaa"
    assert not await user_has_dice(update, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "active_users": ["@aaa", "@bbb"],
        "cycles": [{}, {"points": {"@aaa": {}}}],
    },
)
async def test_user_has_dice_has(*args):
    update = AsyncMock()
    update.effective_user.username = "aaa"
    assert await user_has_dice(update, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "active_users": ["@aaa", "@bbb"],
        "cycles": [{}, {"users": ["@aaa"], "points": {"@aaa": {}}}],
    },
)
async def test_user_can_dice_no(*args):
    update = AsyncMock()
    update.effective_user.username = "aaa"
    assert not await user_can_dice(update, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "active_users": ["@aaa", "@bbb"],
        "cycles": [{}, {"users": ["@aaa"], "points": {}}],
    },
)
async def test_user_can_dice(*args):
    update = AsyncMock()
    update.effective_user.username = "aaa"
    assert await user_can_dice(update, None)


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=False)
async def test_register_point_no_has_open_game(*args):
    assert await register_point(None, None) is False


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch("app.services.chat.get_chat_item", return_value={"cycles": [{}]})
@patch("app.services.chat._user_has_dice", return_value=True)
async def test_register_point_user_has_dice(*args):
    assert await register_point(None, None) is False


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch("app.services.chat.get_chat_item", return_value={"cycles": [{"points": {}}]})
@patch("app.services.chat._user_has_dice", return_value=False)
async def test_register_point(*args):
    context = AsyncMock()
    update = AsyncMock()
    update.effective_user.username = "aaa"
    update.effective_message.id = 5555
    update.message.dice.value = 5
    update.effective_chat.id = 1
    await register_point(update, context)
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={"cycles": [{"points": {"@aaa": {"message_id": 5555, "value": 5}}}]},
    )


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch("app.services.chat.get_chat_item", return_value={"cycles": [{"points": {}}]})
@patch("app.services.chat._user_has_dice", return_value=False)
async def test_register_point_other_message_id_and_value(*args):
    context = AsyncMock()
    update = AsyncMock()
    update.effective_user.username = "aaa"
    update.effective_message.id = 5555
    update.message.dice.value = 5
    update.effective_chat.id = 1
    await register_point(update, context, 6666, 4)
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={"cycles": [{"points": {"@aaa": {"message_id": 6666, "value": 4}}}]},
    )
