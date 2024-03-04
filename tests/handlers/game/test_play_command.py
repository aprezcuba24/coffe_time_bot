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
        username="aaa",
    )
    await play_command(tester.update, tester.context)
    tester.assert_reply_text(
        reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
        text="Hay una partida abierta. ¿La quiere descartar?",
    )


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat(
        {"users": {}, "active_users": ["@aaa", "@bbb"], "cycles": []}, username="aaa"
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


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat(
        {"users": {}, "active_users": [], "cycles": []},
    )
    await play_command(tester.update, tester.context)
    tester.context.application.persistence.update_chat_data.assert_not_called()
    tester.assert_reply_text(
        text="Tu usuario no está activo. Adiciónalo primero.",
    )
