from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardMarkup

from app.handlers.dice import dice_handler, get_buttons
from tests.util import get_chat


@pytest.mark.asyncio
async def test_no_is_active_user():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
        username="bbb",
    )
    await dice_handler(tester.update, tester.context)
    tester.assert_reply_text(text="Tu usuario no está activo. Adiciónalo primero.")


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
        message_id=5555,
        message_value=1,
        username="aaa",
        user_id=111,
    )
    await dice_handler(tester.update, tester.context)
    buttons = get_buttons(111, 5555, 1)
    tester.assert_reply_text(
        reply_markup=InlineKeyboardMarkup([buttons]),
        text="No hay una partida abierta. ¿Quiere abrir una?",
    )


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
    await dice_handler(tester.update, tester.context)
    tester.assert_reply_text(
        text="Ya tiraste el dado.",
    )


@pytest.mark.asyncio
async def test_no_user_can_dice():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"points": {"@aaa": {}}, "users": ["@aaa"]}],
        },
        username="bbb",
    )
    await dice_handler(tester.update, tester.context)
    tester.assert_reply_text(
        text="No puedes votar en esta ronda.",
    )


@pytest.mark.asyncio
async def test_register_point():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"points": {}, "users": ["@aaa", "@bbb"]}],
        },
        username="aaa",
        message_id=5555,
        message_value=5,
    )
    await dice_handler(tester.update, tester.context)
    tester.update.effective_message.reply_text.assert_not_called()
    tester.update._bot.send_message.assert_not_called()
    await tester.assert_save(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "points": {"@aaa": {"message_id": 5555, "value": 5}},
                    "users": ["@aaa", "@bbb"],
                }
            ],
        }
    )


@pytest.mark.asyncio
@patch("time.sleep", return_value=None)
async def test_register_point(*args):
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "points": {"@aaa": {"message_id": 5555, "value": 5}},
                    "users": ["@aaa", "@bbb"],
                }
            ],
        },
        username="bbb",
        message_id=6666,
        message_value=6,
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await dice_handler(tester.update, tester.context)
    tester.update.effective_message.reply_text.assert_not_called()
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {"@aaa": {"data": 1, "score": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )
    bot.send_message.assert_called_once_with(
        chat_id=1, text="Tenemos cafecito ☕️ de @aaa 🏆"
    )
