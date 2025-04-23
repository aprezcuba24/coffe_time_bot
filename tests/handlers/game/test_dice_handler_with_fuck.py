from unittest.mock import patch, AsyncMock

import pytest

from app.handlers.dice import dice_handler
from app.services.fuck_service import FuckService
from tests.util import get_chat


@pytest.mark.asyncio
@patch("app.services.fuck_service.FuckService.process_fuck_triggers")
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_fuck_active(
    mock_sleep, mock_game_over, mock_process_fuck_triggers
):
    """Test dice handler when a user has an active fuck command"""
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 4},
                "@bbb": {"data": 1},
            },
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "points": {"@aaa": {"message_id": 5555, "value": 4}},
                    "users": ["@aaa", "@bbb"],
                }
            ],
            "last_play_date": None,
        },
        username="bbb",
        message_id=6666,
        message_value=3,  # Lower than the fuck_value (4)
    )

    await dice_handler(tester.update, tester.context)

    # Verify that process_fuck_triggers was called with the correct arguments
    mock_process_fuck_triggers.assert_called_once_with(
        update=tester.update,
        users_data=tester.chat._users,
        current_username="@bbb",
        current_dice_value=3,
    )

    # The fuck_active should be set to False after use (handled by process_fuck_triggers)
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 4},
                "@bbb": {"data": 1, "score": 1},
            },
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
@patch("app.services.fuck_service.FuckService.process_fuck_triggers")
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_fuck_not_triggered(
    mock_sleep, mock_game_over, mock_process_fuck_triggers
):
    """Test dice handler when a user has an active fuck command but the dice value is higher"""
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 2},
                "@bbb": {"data": 1},
            },
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "points": {"@aaa": {"message_id": 5555, "value": 2}},
                    "users": ["@aaa", "@bbb"],
                }
            ],
            "last_play_date": None,
        },
        username="bbb",
        message_id=6666,
        message_value=5,  # Higher than the fuck_value (2), so it shouldn't trigger
    )

    await dice_handler(tester.update, tester.context)

    # Verify that process_fuck_triggers was called with the correct arguments
    mock_process_fuck_triggers.assert_called_once_with(
        update=tester.update,
        users_data=tester.chat._users,
        current_username="@bbb",
        current_dice_value=5,
    )

    # The fuck_active should still be True (handled by process_fuck_triggers)
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 2, "score": 1},
                "@bbb": {"data": 1},
            },
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
@patch("app.services.fuck_service.FuckService.process_fuck_triggers")
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_multiple_fuck_active(
    mock_sleep, mock_game_over, mock_process_fuck_triggers
):
    """Test dice handler when multiple users have active fuck commands"""
    tester = await get_chat(
        {
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 4},
                "@bbb": {"data": 1},
                "@ccc": {"data": 1, "fuck_active": True, "fuck_value": 3},
            },
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "points": {
                        "@aaa": {"message_id": 5555, "value": 4},
                        "@ccc": {"message_id": 7777, "value": 3},
                    },
                    "users": ["@aaa", "@bbb", "@ccc"],
                }
            ],
            "last_play_date": None,
        },
        username="bbb",
        message_id=6666,
        message_value=2,  # Lower than both fuck_values, should trigger both
    )

    await dice_handler(tester.update, tester.context)

    # Verify that process_fuck_triggers was called with the correct arguments
    mock_process_fuck_triggers.assert_called_once_with(
        update=tester.update,
        users_data=tester.chat._users,
        current_username="@bbb",
        current_dice_value=2,
    )

    # Both fuck_active flags should be set to False after use (handled by process_fuck_triggers)
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"data": 1, "fuck_active": True, "fuck_value": 4},
                "@bbb": {"data": 1, "score": 1},
                "@ccc": {"data": 1, "fuck_active": True, "fuck_value": 3},
            },
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [],
        }
    )
