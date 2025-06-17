import pytest

from app.handlers.who_are_left import who_are_left_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_no_open_game():
    tester = await get_chat({})
    await who_are_left_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay juego abierto")


@pytest.mark.asyncio
async def test_no_one_is_missing():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"message_id": 1111, "value": 1},
                        "@bbb": {"message_id": 1111, "value": 1},
                        "@ccc": {"message_id": 1111, "value": 2},
                    },
                }
            ],
        },
    )
    await who_are_left_command(tester.update, tester.context)
    tester.assert_reply_text(text="No Falta nadie")


@pytest.mark.asyncio
async def test_no_one_is_missing():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"message_id": 1111, "value": 1},
                    },
                }
            ],
        },
    )
    await who_are_left_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="Todavía faltan por tirar @bbb @ccc\nLos perdedores hasta ahora, con 1 son: @aaa"
    )
