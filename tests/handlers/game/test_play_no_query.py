from unittest.mock import AsyncMock

import pytest

from app.handlers.game import play_no_query


@pytest.mark.asyncio
async def test_no():
    update = AsyncMock()
    await play_no_query(update)
    update.effective_message.edit_text.assert_called_once_with(
        text="Ok el juego se mantiene activo.",
    )
