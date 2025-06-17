from unittest.mock import AsyncMock

import pytest
from telegram import InlineKeyboardMarkup

from app.handlers.abort import (
    NO_BUTTON,
    YES_BUTTON,
    abort_command,
    abort_no_query,
    abort_yes_query,
)
from tests.util import get_chat


@pytest.mark.asyncio
async def test_user_no_active():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]}, username="bbb"
    )
    assert await abort_command(tester.update, tester.context)
    tester.assert_reply_text(text="Tu usuario no está activo. Adiciónalo primero.")


@pytest.mark.asyncio
async def test_user_no_open_game():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]}, username="aaa"
    )
    assert await abort_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay partida abierta.")


@pytest.mark.asyncio
async def test_has_open_game():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {"@aaa": {"value": 1}, "@bbb": {"value": 2}},
                }
            ],
        },
        username="bbb",
    )
    assert await abort_command(tester.update, tester.context)
    tester.assert_reply_text(
        reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
        text="¿Está seguro, quiere abortar el juego?",
    )


@pytest.mark.asyncio
async def test_is_losing():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {"@aaa": {"value": 1}, "@bbb": {"value": 2}},
                }
            ],
        },
        username="aaa",
    )
    assert await abort_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="No puedes abortar el juego, si estás perdiendo. 😏",
    )


@pytest.mark.asyncio
async def test_abort_no_query():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert await abort_no_query(tester.update, tester.context)
    tester.assert_edit_text(text="Ok el juego se mantiene activo.")


@pytest.mark.asyncio
async def test_abort_yes_query():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {"@aaa": {}}}],
        },
        username="aaa",
    )
    assert await abort_yes_query(tester.update, tester.context)
    tester.assert_edit_text(text="El juego fue abortado por @aaa")
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [],
        }
    )
