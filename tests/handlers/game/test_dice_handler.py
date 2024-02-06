from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardMarkup

from app.handlers.dice import dice_handler, get_buttons


@pytest.mark.asyncio
@patch("app.handlers.dice.is_active_user", return_value=False)
async def test_no_is_active_user(*args):
    update = AsyncMock()
    await dice_handler(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="Tu usuario no está activo. Adiciónalo primero."
    )


@pytest.mark.asyncio
@patch("app.handlers.dice.is_active_user", return_value=True)
@patch("app.handlers.dice.has_open_game", return_value=False)
async def test_no_has_open_game(*args):
    update = AsyncMock()
    update.effective_message.id = 5555
    update.message.dice.value = 1
    await dice_handler(update, None)
    buttons = get_buttons(update.effective_message.id, update.message.dice.value)
    update.effective_message.reply_text.assert_called_once_with(
        reply_markup=InlineKeyboardMarkup([buttons]),
        text="No hay una partida abierta. ¿Quiere abrir una?",
    )


@pytest.mark.asyncio
@patch("app.handlers.dice.is_active_user", return_value=True)
@patch("app.handlers.dice.has_open_game", return_value=True)
@patch("app.handlers.dice.user_has_dice", return_value=True)
async def test_user_has_dice(*args):
    update = AsyncMock()
    await dice_handler(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="Ya tiraste el dado.",
    )


@pytest.mark.asyncio
@patch("app.handlers.dice.is_active_user", return_value=True)
@patch("app.handlers.dice.has_open_game", return_value=True)
@patch("app.handlers.dice.user_has_dice", return_value=False)
@patch("app.handlers.dice.user_can_dice", return_value=False)
async def test_no_user_can_dice(*args):
    update = AsyncMock()
    await dice_handler(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="No puedes votar en esta ronda.",
    )


@pytest.mark.asyncio
@patch("app.handlers.dice.is_active_user", return_value=True)
@patch("app.handlers.dice.has_open_game", return_value=True)
@patch("app.handlers.dice.user_has_dice", return_value=False)
@patch("app.handlers.dice.user_can_dice", return_value=True)
@patch("app.handlers.dice.register_point")
async def test_register_point(register_point_mock, *args):
    update = AsyncMock()
    context = AsyncMock()
    await dice_handler(update, context)
    update.effective_message.reply_text.assert_not_called()
    register_point_mock.assert_called_once_with(update, context)
