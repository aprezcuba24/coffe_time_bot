import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.fuck_service import FuckService


def test_get_users_to_trigger():
    # Test with no users to trigger
    current_username = "@current"
    users_data = {
        "@current": {"data": 1},
        "@user1": {"data": 1},
        "@user2": {"data": 1, "fuck_active": True, "fuck_value": 2},
    }
    current_dice_value = 3  # Higher than the fuck_value

    result = FuckService.get_users_to_trigger(current_username, users_data, current_dice_value)
    assert result == []

    # Test with one user to trigger
    current_dice_value = 2  # Equal to the fuck_value
    result = FuckService.get_users_to_trigger(current_username, users_data, current_dice_value)
    assert result == ["@user2"]

    # Test with two users to trigger
    users_data["@user3"] = {"data": 1, "fuck_active": True, "fuck_value": 3}
    result = FuckService.get_users_to_trigger(current_username, users_data, current_dice_value)
    assert result == ["@user2", "@user3"]


def test_get_random_reaction():
    # Test that the function returns a tuple of two strings
    with patch("random.choice", side_effect=["💩", "¡Te jodieron!"]):
        emoji, reaction = FuckService.get_random_reaction()
        assert emoji == "💩"
        assert reaction == "¡Te jodieron!"


def test_deactivate_fuck_commands():
    # Test that the function deactivates fuck commands
    users_data = {
        "@user1": {"data": 1, "fuck_active": True, "fuck_value": 2},
        "@user2": {"data": 1, "fuck_active": True, "fuck_value": 3},
        "@user3": {"data": 1},
    }
    usernames = ["@user1", "@user2", "@nonexistent"]

    FuckService.deactivate_fuck_commands(users_data, usernames)

    assert users_data["@user1"]["fuck_active"] is False
    assert users_data["@user2"]["fuck_active"] is False
    # @user3 should not be affected
    assert "fuck_active" not in users_data["@user3"]


def test_get_angry_emotes():
    # Test that the function returns a tuple of two strings
    with patch("random.sample", return_value=["💢", "😡", "😤"]):
        with patch("random.choice", return_value="maldición"):
            emojis, symbol = FuckService.get_angry_emotes()
            assert emojis == "💢 😡 😤"
            assert symbol == "maldición"


def test_is_valid_dice_value():
    # Test that the function correctly identifies valid dice values
    assert FuckService.is_valid_dice_value(1) is True
    assert FuckService.is_valid_dice_value(2) is True
    assert FuckService.is_valid_dice_value(3) is False
    assert FuckService.is_valid_dice_value(0) is False


@pytest.mark.asyncio
async def test_process_fuck_triggers():
    # Test with no users to trigger
    update = AsyncMock()
    users_data = {
        "@current": {"data": 1},
        "@user1": {"data": 1, "fuck_active": True, "fuck_value": 2},
    }
    current_username = "@current"
    current_dice_value = 3  # Higher than the fuck_value

    with patch.object(FuckService, "get_users_to_trigger", return_value=[]):
        await FuckService.process_fuck_triggers(update, users_data, current_username, current_dice_value)
        update.effective_message.reply_text.assert_not_called()

    # Test with users to trigger
    with patch.object(FuckService, "get_users_to_trigger", return_value=["@user1"]):
        with patch.object(FuckService, "get_random_reaction", return_value=("💩", "¡Te jodieron!")):
            with patch.object(FuckService, "deactivate_fuck_commands") as mock_deactivate:
                await FuckService.process_fuck_triggers(update, users_data, current_username, current_dice_value)
                update.effective_message.reply_text.assert_called_once_with(
                    text="¡Te jodieron! 💩 @user1 está disfrutando tu infortunio."
                )
                mock_deactivate.assert_called_once_with(users_data, ["@user1"]) 