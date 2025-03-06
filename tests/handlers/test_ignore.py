import pytest

from app.handlers.ignore import ignore_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_ignore():
    tester = await get_chat({})
    await ignore_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay juego abierto.")


@pytest.mark.asyncio
async def test_user_has_dice():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"points": {"@aaa": {}}, "users": ["@aaa"]}],
        },
        username="aaa",
    )
    await ignore_command(tester.update, tester.context)
    tester.assert_reply_text(text="Ya lanzó el dado.")


@pytest.mark.asyncio
async def test_no_in_play():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [{"points": {"@aaa": {}}, "users": ["@aaa", "@bbb"]}],
        },
        username="ccc",
    )
    await ignore_command(tester.update, tester.context)
    tester.assert_reply_text(text="No tiene que lanzar el dado.")


@pytest.mark.asyncio
async def test_no_is_the_first_cycle():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {"points": {"@aaa": {}}, "users": ["@aaa", "@bbb"]},
                {"points": {"@aaa": {}}, "users": ["@aaa", "@bbb"]},
            ],
        },
        username="ccc",
    )
    await ignore_command(tester.update, tester.context)
    tester.assert_reply_text(text="Solo se puede ignorar en el primer ciclo.")


@pytest.mark.asyncio
async def test_ignore():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [{"points": {"@aaa": {}}, "users": ["@aaa", "@bbb", "@ccc"]}],
        },
        username="ccc",
    )
    await ignore_command(tester.update, tester.context)
    tester.assert_reply_text(text="Ya fuiste ignorado. Que no te vea tomando café 😡")
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [{"points": {"@aaa": {}}, "users": ["@aaa", "@bbb"]}],
        }
    )
