from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.handlers.add_user import add_user_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_not_args():
    tester = await get_chat({}, args=[])
    await add_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="Debe pasar almenos un usuario.")


@pytest.mark.asyncio
async def test_a_arg_is_not_a_username():
    tester = await get_chat({}, args=["@aaa", "aaa"])
    await add_user_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="Estos valores no son usuarios válidos de telegram: aaa"
    )


@pytest.mark.asyncio
async def test_complete():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
        args=["@aaa", "@bbb"],
    )
    await add_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="Los usuarios fueron añadidos.")
    tester.assert_save(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
        }
    )
