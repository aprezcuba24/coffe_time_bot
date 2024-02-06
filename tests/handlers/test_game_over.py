from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.game_over import game_over_command


@pytest.mark.asyncio
@patch("app.handlers.game_over.game_over", return_value=None)
async def test_no_open_game(*args):
    update = AsyncMock()
    assert await game_over_command(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="No hay ningún juego abierto."
    )


@pytest.mark.asyncio
@patch("app.handlers.game_over.game_over", return_value=["@aaa"])
async def test_has_a_winner(*args):
    update = AsyncMock()
    assert await game_over_command(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="Tenemos un ganador @aaa"
    )


@pytest.mark.asyncio
@patch("app.handlers.game_over.game_over", return_value=["@aaa", '@bbb'])
async def test_a_new_cycle(*args):
    update = AsyncMock()
    assert await game_over_command(update, None)
    update.effective_message.reply_text.assert_called_once_with(
        text="Desempate @aaa @bbb"
    )
