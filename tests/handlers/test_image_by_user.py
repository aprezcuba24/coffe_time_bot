import pytest

from app.handlers.manage_user_image import images_by_users_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_images_by_users():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        }
    )
    await images_by_users_command(tester.update, tester.context)
    tester.assert_send_photo(photo="a_value", caption="@aaa")
