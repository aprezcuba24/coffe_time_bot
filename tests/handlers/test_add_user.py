from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.handlers.add_user import add_user_command


@pytest.mark.asyncio
async def test_not_args():
    update = MagicMock()
    context = MagicMock()
    context.args = []
    await add_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="Debe pasar almenos un usuario."
    )


@pytest.mark.asyncio
async def test_a_arg_is_not_a_username():
    update = MagicMock()
    context = MagicMock()
    context.args = ["@aaa", "aaa"]
    await add_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="Estos valores no son usuarios válidos de telegram: aaa"
    )


@pytest.mark.asyncio
@patch(
    "app.handlers.add_user.get_chat_item",
    return_value={"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
)
async def test_complete(*args):
    update = AsyncMock()
    context = AsyncMock()
    context.args = ["@aaa", "@bbb"]
    update.effective_chat.id = 1
    await add_user_command(update, context)
    update.effective_message.reply_text.assert_called_once_with(
        text="Los usuarios fueron añadidos."
    )
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        },
    )
