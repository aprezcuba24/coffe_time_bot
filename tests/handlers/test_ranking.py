import pytest
from telegram.constants import ParseMode

from app.handlers.ranking import ranking_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_not_ranking():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {}},
        }
    )
    await ranking_command(tester.update, tester.context)
    tester.assert_reply_text(text="Todavía no hay ranking")


@pytest.mark.asyncio
async def test_ranking():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"score": 1},
                "@bbb": {"score": 2},
                "@ccc": {},
                "@ddd": {"score": 3},
                "@eee": {"score": 4},
            },
        }
    )
    await ranking_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="🥇 @eee 👉 4\n🥈 @ddd 👉 3\n🥉 @bbb 👉 2\n🔸 @aaa 👉 1",
    )
