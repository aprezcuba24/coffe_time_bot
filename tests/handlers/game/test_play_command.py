from unittest.mock import AsyncMock, patch

import pytest
from telegram import InlineKeyboardMarkup

from app.handlers.game import NO_BUTTON, YES_BUTTON, play_command


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={"cycles": [{}]},
)
async def test_has_open_game(*args):
    update = AsyncMock()
    context = AsyncMock()
    await play_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        reply_markup=InlineKeyboardMarkup([[YES_BUTTON, NO_BUTTON]]),
        text="Hay una partida abierta. ¿La quiere descartar?",
    )


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={"cycles": [], "active_users": ["@aaa", "@bbb"]},
)
async def test_no_has_open_game(*args):
    update = AsyncMock()
    update.effective_chat.id = 1
    context = AsyncMock()
    await play_command(update, context)
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
            "active_users": ["@aaa", "@bbb"],
        },
    )
    update.effective_message.reply_text.assert_called_once_with(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
