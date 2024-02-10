from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardMarkup

from app.handlers.game import NO_BUTTON, YES_BUTTON, play_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_has_open_game():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"users": [], "points": {}}],
        },
    )
    await play_command(tester.update, tester.context)
    tester.assert_reply_text(
        reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
        text="Hay una partida abierta. ¿La quiere descartar?",
    )


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat(
        {"users": {}, "active_users": ["@aaa", "@bbb"], "cycles": []},
    )
    await play_command(tester.update, tester.context)
    await tester.assert_save(
        data={
            "users": {},
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
            "active_users": ["@aaa", "@bbb"],
        },
    )
    tester.assert_reply_text(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
