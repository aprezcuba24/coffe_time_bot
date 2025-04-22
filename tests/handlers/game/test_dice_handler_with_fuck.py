from unittest.mock import patch, AsyncMock

import pytest

from app.handlers.dice import dice_handler
from tests.util import get_chat


@pytest.mark.asyncio
@patch("random.choice", side_effect=["💩", "¡Te jodieron!"])
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_fuck_active(mock_sleep, mock_game_over, mock_random_choice):
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
    
    # Should trigger the fuck message
    tester.update.effective_message.reply_text.assert_any_call(
        text="¡Te jodieron! 💩 @aaa está disfrutando tu infortunio."
    )
    
    # The fuck_active should be set to False after use
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"data": 1, "fuck_active": False, "fuck_value": 4},
                "@bbb": {"data": 1, "score": 1},
            },
            "active_users": ["@aaa", "@bbb"],
            "cycles": [],
        }
    )


@pytest.mark.asyncio
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_fuck_not_triggered(mock_sleep, mock_game_over):
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
    
    # Get all calls to reply_text
    call_args_list = tester.update.effective_message.reply_text.call_args_list
    
    # Make sure no fuck message was sent
    for call in call_args_list:
        args, kwargs = call
        if kwargs.get('text') and 'jodieron' in kwargs.get('text'):
            pytest.fail("Fuck message was triggered when it shouldn't have been")
    
    # The fuck_active should still be True
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
@patch("random.choice", side_effect=["🤡", "¡Qué mal número, te han jodido!"])
@patch("app.handlers.dice.game_over_message", return_value=None)
@patch("time.sleep", return_value=None)
async def test_dice_handler_with_multiple_fuck_active(mock_sleep, mock_game_over, mock_random_choice):
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
    
    # Should trigger the fuck message from both users
    tester.update.effective_message.reply_text.assert_any_call(
        text="¡Qué mal número, te han jodido! 🤡 @aaa @ccc está disfrutando tu infortunio."
    )
    
    # Both fuck_active flags should be set to False after use
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {
                "@aaa": {"data": 1, "fuck_active": False, "fuck_value": 4},
                "@bbb": {"data": 1, "score": 1},
                "@ccc": {"data": 1, "fuck_active": False, "fuck_value": 3},
            },
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [],
        }
    ) 