from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.handlers.remove_user import remove_user_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_not_args():
    tester = await get_chat({}, args=[])
    await remove_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="Debe pasar solo un usuario.")


@pytest.mark.asyncio
async def test_more_than_one():
    tester = await get_chat({}, args=["@aaa", "@bbb"])
    await remove_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="Debe pasar solo un usuario.")


@pytest.mark.asyncio
async def test_is_not_valid_username():
    tester = await get_chat({}, args=["aaa"])
    await remove_user_command(tester.update, tester.context)
    tester.assert_reply_text(text='Este valor "aaa" no es un usuario válido.')


@pytest.mark.asyncio
async def test_complete():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        },
        args=["@bbb"],
    )
    await remove_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="El usuario @bbb fue eleminado.")
    await tester.assert_save(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa"],
            "cycles": [],
        }
    )
