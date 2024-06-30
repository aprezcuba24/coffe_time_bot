import os

import pytest
from telegram import PhotoSize

from app.handlers.manage_user_image import (
    image_of_user_command,
    images_by_users_command,
    upload_photo,
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


@pytest.mark.asyncio
async def test_upload_image_user_not_exists():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        caption="@ddd",
        username="username_enter",
    )
    await upload_photo(tester.update, tester.context)
    tester.assert_reply_text(text="El usuario no existe.")


@pytest.mark.asyncio
async def test_upload_image_user():
    photo = [None, None, None, PhotoSize("file_id_mock", "", 2, 2)]
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        },
        caption="@bbb",
        username="username_enter",
        photo=photo,
    )
    await upload_photo(tester.update, tester.context)
    tester.assert_reply_text(text="Hecho.")
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": "file_id_mock"},
                "@ccc": {},
            },
            "active_users": [],
            "cycles": [],
        }
    )
