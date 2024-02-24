from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.game import play_yes_query
from tests.util import get_chat


@pytest.mark.asyncio
async def test_yes():
    tester = await get_chat(
        {
            "users": {},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@ccc", "@ddd"], "points": {}}],
        },
    )
    await play_yes_query(tester.update, tester.context)
    await tester.assert_save(
        {
            "users": {},
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
            "active_users": ["@aaa", "@bbb"],
        }
    )
    tester.assert_edit_text(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
