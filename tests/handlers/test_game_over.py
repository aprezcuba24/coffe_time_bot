from unittest.mock import AsyncMock

import pytest

from app.handlers.game_over import game_over_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_user_no_active():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]}, username="bbb"
    )
    assert await game_over_command(tester.update, tester.context)
    tester.assert_reply_text(text="Tu usuario no está activo. Adiciónalo primero.")


@pytest.mark.asyncio
async def test_no_open_game():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]}, username="aaa"
    )
    assert await game_over_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay ningún juego abierto o no se llegó a jugar.")


@pytest.mark.asyncio
async def test_has_a_winner():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {
                        "@aaa": {"message_id": 1111, "value": 1},
                        "@bbb": {"message_id": 1111, "value": 2},
                    },
                }
            ],
        },
        username="aaa",
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await game_over_command(tester.update, tester.context)
    bot.send_message.assert_called_once_with(chat_id=1, text="Tenemos tenemos cafecito ☕️ de @aaa 🏆")


@pytest.mark.asyncio
async def test_a_new_cycle():
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
        username="aaa",
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await game_over_command(tester.update, tester.context)
    bot.send_message.assert_called_once_with(chat_id=1, text="Desempate @aaa @bbb")


@pytest.mark.asyncio
async def test_no_dice():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {},
                }
            ],
        },
        username="aaa",
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await game_over_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay ningún juego abierto o no se llegó a jugar.")
