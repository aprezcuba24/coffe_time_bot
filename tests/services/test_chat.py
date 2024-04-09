from collections import defaultdict
from datetime import datetime

import pytest

from tests.util import get_chat


@pytest.mark.asyncio
async def test_add_user_it_there():
    tester = await get_chat({"users": {"@aaa": {}}, "active_users": ["@aaa"]})
    tester.chat.add_user("@bbb")
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_remove_user():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        }
    )
    tester.chat.remove_user("@bbb")
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_get_chat_item_not_chat():
    tester = await get_chat(defaultdict(dict, {}))
    tester.assert_chat_data(
        {"last_play_date": None, "users": {}, "active_users": [], "cycles": []}
    )


@pytest.mark.asyncio
async def test_get_chat_item_has_chat():
    tester = await get_chat(
        {"users": {"@aaaa": {}}, "active_users": ["@aaaa"], "cycles": []}
    )
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaaa": {}},
            "active_users": ["@aaaa"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat({"cycles": []})
    assert not tester.chat.has_open_game()


@pytest.mark.asyncio
async def test_has_open_game():
    tester = await get_chat({"cycles": [{"users": [], "points": {}}]})
    assert tester.chat.has_open_game()


@pytest.mark.asyncio
async def test_open_game():
    tester = await get_chat(
        {"active_users": ["@aaa", "@bbb"], "cycles": [{"users": [], "points": {}}]}
    )
    users = tester.chat.open_game()
    assert users == ["@aaa", "@bbb"]
    tester.assert_chat_data(
        {
            "last_play_date": datetime.now().isoformat(timespec="minutes"),
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
        }
    )


@pytest.mark.asyncio
async def test_no_is_active_user():
    tester = await get_chat({"active_users": ["@aaa", "@bbb"]}, username="ccc")
    assert not tester.chat.is_active_user()


@pytest.mark.asyncio
async def test_is_active_user(*args):
    tester = await get_chat({"active_users": ["@aaa", "@bbb"]}, username="aaa")
    assert tester.chat.is_active_user()


@pytest.mark.asyncio
async def test_user_has_dice_no_has_open_game():
    tester = await get_chat({})
    assert not tester.chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_has_dice_no_has():
    tester = await get_chat(
        {"active_users": ["@aaa", "@bbb"], "cycles": [{"points": {}, "users": []}]},
        username="aaa",
    )
    assert not tester.chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_has_dice_has():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": {}, "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert tester.chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_has_dice_other_user():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {"@bbb": {"message_id": 7641, "value": 5}},
                }
            ],
        },
        username="aaa",
    )
    assert not tester.chat.user_has_dice()


@pytest.mark.asyncio
async def test_user_can_dice_no():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert not tester.chat.user_can_dice()


@pytest.mark.asyncio
async def test_user_can_dice():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
    )
    assert tester.chat.user_can_dice()


@pytest.mark.asyncio
async def test_register_point_no_has_open_game():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        },
    )
    assert tester.chat.register_point() is False


@pytest.mark.asyncio
async def test_register_point_user_has_dice():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert tester.chat.register_point() is False


@pytest.mark.asyncio
async def test_register_point():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
        message_id=5555,
        message_value=5,
    )
    tester.chat.register_point()
    tester.assert_chat_data(
        {
            "last_play_date": None,
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
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa"], "points": {}}],
        },
        username="aaa",
        message_id=5555,
        message_value=5,
    )
    tester.chat.register_point(message_id=6666, value=6)
    tester.assert_chat_data(
        {
            "last_play_date": None,
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
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
    )
    assert tester.chat.is_the_last_user() is False


@pytest.mark.asyncio
async def test_is_the_last():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}, "@bbb": {}}}],
        },
    )
    assert tester.chat.is_the_last_user()


@pytest.mark.asyncio
async def test_who_are_left_no_open_game():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        },
    )
    assert tester.chat.who_are_left() == None


@pytest.mark.asyncio
async def test_who_are_left_all():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
        },
    )
    assert tester.chat.who_are_left() == ["@aaa", "@bbb"]


@pytest.mark.asyncio
async def test_who_are_left_one():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
    )
    assert tester.chat.who_are_left() == ["@bbb"]


@pytest.mark.asyncio
async def test_abort():
    tester = await get_chat(
        {
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
    )
    tester.chat.abort()
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )
