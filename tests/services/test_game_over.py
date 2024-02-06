from unittest.mock import AsyncMock, patch

import pytest

from app.services.chat import game_over


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=False)
async def test_no_open_game(*args):
    assert await game_over(None, None) is None


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "cycles": [
            {
                "points": {
                    "@aaa": {"value": 2},
                    "@bbb": {"value": 2},
                    "@ccc": {"value": 3},
                }
            }
        ]
    },
)
async def test_more_than_one_user(*args):
    context = AsyncMock()
    update = AsyncMock()
    update.effective_chat.id = 1
    assert await game_over(update, context) == ["@aaa", "@bbb"]
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={
            "cycles": [
                {
                    "points": {
                        "@aaa": {"value": 2},
                        "@bbb": {"value": 2},
                        "@ccc": {"value": 3},
                    }
                },
                {"users": ["@aaa", "@bbb"], "points": {}},
            ]
        },
    )


@pytest.mark.asyncio
@patch("app.services.chat.has_open_game", return_value=True)
@patch(
    "app.services.chat.get_chat_item",
    return_value={
        "users": {},
        "cycles": [
            {
                "points": {
                    "@aaa": {"value": 5},
                    "@bbb": {"value": 4},
                    "@ccc": {"value": 3},
                }
            }
        ],
    },
)
async def test_has_a_winner(*args):
    context = AsyncMock()
    update = AsyncMock()
    update.effective_chat.id = 1
    assert await game_over(update, context) == ["@ccc"]
    context.application.persistence.update_chat_data.assert_called_once_with(
        chat_id=1,
        data={"cycles": [], "users": {"@ccc": {"score": 1}}},
    )
