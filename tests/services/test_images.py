import pytest

from tests.util import get_chat


@pytest.mark.asyncio
async def test_images_by_user_empty():
    tester = await get_chat(None)
    assert tester.chat.images_by_user() == []


@pytest.mark.asyncio
async def test_images_by_user():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        }
    )
    assert tester.chat.images_by_user() == [("@aaa", "a_value")]


@pytest.mark.asyncio
async def test_image_of_user():
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"image": "a_value"},
                "@bbb": {"image": None},
                "@ccc": {},
            },
        }
    )
    assert tester.chat.image_of_user("@aaa") == "a_value"
    assert tester.chat.image_of_user("@bbb") == None
    assert tester.chat.image_of_user("@ccc") == None
