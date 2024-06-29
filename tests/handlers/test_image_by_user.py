import os

import pytest

from app.handlers.manage_user_image import (
    image_of_user_command,
    images_by_users_command,
)
from tests.util import get_chat

os.environ = {"ADMIN_USERS": "username_enter"}


@pytest.mark.asyncio
async def test_not_access():
    tester = await get_chat({}, username="username_enter_other")
    await images_by_users_command(tester.update, tester.context)
    tester.assert_reply_text(text="No tiene acceso a esta funcionalidad.")


@pytest.mark.asyncio
async def test_images_by_users():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        username="username_enter",
    )
    await images_by_users_command(tester.update, tester.context)
    tester.assert_send_photo(photo="a_value", caption="@aaa")


@pytest.mark.asyncio
async def test_image_of_users_none():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        args=["@ccc"],
        username="username_enter",
    )
    await image_of_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay imagen")


@pytest.mark.asyncio
async def test_image_of_users_no_exits():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        args=["@ddd"],
        username="username_enter",
    )
    await image_of_user_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay imagen")


@pytest.mark.asyncio
async def test_image_of_user():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        args=["@aaa"],
        username="username_enter",
    )
    await image_of_user_command(tester.update, tester.context)
    tester.assert_reply_photo(photo="a_value")
