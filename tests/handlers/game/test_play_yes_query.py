from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.game import play_yes_query


@pytest.mark.asyncio
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "cycles": [{"users": ["@ccc", "@ddd"], "points": {}}],
        "active_users": ["@aaa", "@bbb"],
    },
)
async def test_yes(*args):
    update = AsyncMock()
    update.effective_chat.id = 1
    context = AsyncMock()
    await play_yes_query(update, context)
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={
            "cycles": [{"users": ["@aaa", "@bbb"], "points": {}}],
            "active_users": ["@aaa", "@bbb"],
        },
    )
    update.effective_message.edit_text.assert_called_once_with(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
