from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.dice import yes_play_dice_query
from tests.util import get_chat


@pytest.mark.asyncio
async def test_has_open_game():
    tester = await get_chat(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@ccc", "@ddd"], "points": {}}],
        },
    )
    assert await yes_play_dice_query(tester.update, tester.context) is None


@pytest.mark.asyncio
async def test_new_game():
    tester = await get_chat(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        },
        callback_query_data="dice_yes_play/7525/5",
        username="aaa",
    )
    await yes_play_dice_query(tester.update, tester.context)
    tester.assert_edit_text(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
    await tester.assert_save(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {"@aaa": {"message_id": 7525, "value": 5}},
                }
            ],
        }
    )
