from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.handlers.remove_user import remove_user_command


@pytest.mark.asyncio
async def test_not_args():
    update = MagicMock()
    context = MagicMock()
    context.args = []
    await remove_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="Debe pasar solo un usuario."
    )


@pytest.mark.asyncio
async def test_more_than_one():
    update = MagicMock()
    context = MagicMock()
    context.args = ["@aaa", "@bbb"]
    await remove_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="Debe pasar solo un usuario."
    )


@pytest.mark.asyncio
async def test_is_not_valid_username():
    update = MagicMock()
    context = MagicMock()
    context.args = ["aaa"]
    await remove_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text='Este valor "aaa" no es un usuario válido.'
    )


@pytest.mark.asyncio
@patch(
    "app.handlers.remove_user.get_chat_item",
    return_value={
        "users": {"@aaa": {"data": 1}, "@bbb": {}},
        "active_users": ["@aaa", "@bbb"],
    },
)
async def test_complete(*agrs):
    update = AsyncMock()
    context = AsyncMock()
    context.args = ["@bbb"]
    update.effective_chat.id = 1
    await remove_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="El usuario @bbb fue eleminado."
    )
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={"users": {"@aaa": {"data": 1}, "@bbb": {}}, "active_users": ["@aaa"]},
    )
