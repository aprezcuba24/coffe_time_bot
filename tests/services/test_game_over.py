import pytest

from tests.util import get_chat


@pytest.mark.asyncio
async def test_no_open_game(*args):
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        }
    )
    try:
        tester.chat.game_over()
        assert False
    except Exception as e:
        assert True


@pytest.mark.asyncio
async def test_more_than_one_user():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"value": 2},
                        "@bbb": {"value": 2},
                        "@ccc": {"value": 3},
                    },
                }
            ],
        }
    )
    assert tester.chat.game_over() == [("@aaa", {}), ("@bbb", {})]
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaa": {}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"value": 2},
                        "@bbb": {"value": 2},
                        "@ccc": {"value": 3},
                    },
                },
                {"users": ["@aaa", "@bbb"], "points": {}},
            ],
        }
    )


@pytest.mark.asyncio
async def test_has_a_winner():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"value": 5},
                        "@bbb": {"value": 4},
                        "@ccc": {"value": 3},
                    },
                }
            ],
        }
    )
    assert tester.chat.game_over() == [("@ccc", {"score": 1})]
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {"score": 1}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
async def test_no_send_dice():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {},
                }
            ],
        }
    )
    assert tester.chat.game_over() == None
    tester.assert_chat_data(
        {
            "last_play_date": None,
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {},
                }
            ],
        }
    )
