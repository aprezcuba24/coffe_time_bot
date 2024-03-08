import pytest

from tests.util import get_chat


@pytest.mark.asyncio
async def test_not_users():
    tester = await get_chat(None)
    assert tester.chat.ranking() == []


@pytest.mark.asyncio
async def test_not_score():
    tester = await get_chat(
        {
            "users": {"@aaa": {}, "@bbb": {}, "@ccc": {}},
        }
    )
    assert tester.chat.ranking() == []


@pytest.mark.asyncio
async def test_two_has_score():
    tester = await get_chat(
        {
            "users": {"@aaa": {"score": 1}, "@bbb": {"score": 2}, "@ccc": {}},
        }
    )
    assert tester.chat.ranking() == [("@bbb", 2), ("@aaa", 1)]
