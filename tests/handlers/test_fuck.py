import pytest
from unittest.mock import patch, ANY

from app.handlers.fuck import fuck_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_no_is_active_user():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
        username="bbb",
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(text="Tu usuario no está activo. Adiciónalo primero.")


@pytest.mark.asyncio
async def test_no_has_open_game():
    tester = await get_chat(
        {"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]},
        username="aaa",
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="No hay una partida abierta. Inicia una con /play primero."
    )


@pytest.mark.asyncio
async def test_no_has_dice():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"points": {}, "users": ["@aaa"]}],
        },
        username="aaa",
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(text="Debes lanzar el dado primero.")


@pytest.mark.asyncio
async def test_success():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"points": {"@aaa": {"message_id": 123, "value": 2}}, "users": ["@aaa"]}],
            "last_play_date": None,
        },
        username="aaa",
        message_value=2,
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="¡Preparado para joder! 😈 Cuando alguien saque 2 o menos, recibirá tu maldición."
    )
    await tester.assert_save(
        {
            "last_play_date": None,
            "users": {"@aaa": {"data": 1, "fuck_active": True, "fuck_value": 2}},
            "active_users": ["@aaa"],
            "cycles": [{"users": ["@aaa"], "points": {"@aaa": {"message_id": 123, "value": 2}}}],
        }
    )


@pytest.mark.asyncio
@patch("random.sample", return_value=["💢", "😡", "😤"])
@patch("random.choice", return_value="maldición")
async def test_user_has_lost(mock_choice, mock_sample):
    """Test that when a user has lost (has a score), they just send angry emojis"""
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1, "score": 2}},  # User has a score, meaning they've lost
            "active_users": ["@aaa"],
            "last_play_date": None,
        },
        username="aaa",
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="💢 😡 😤 maldición 💢 😡 😤"
    )
    # No need to check for save as it doesn't save anything in this case 


@pytest.mark.asyncio
async def test_already_active():
    """Test that when a user tries to use the command twice, they get the 'No te pases!' message"""
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1, "fuck_active": True, "fuck_value": 2}},  # Already has fuck_active
            "active_users": ["@aaa"],
            "cycles": [{"points": {"@aaa": {"message_id": 123, "value": 2}}, "users": ["@aaa"]}],
            "last_play_date": None,
        },
        username="aaa",
        message_value=2,
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="¡No te pases! 🤡"
    )


@pytest.mark.asyncio
async def test_dice_value_not_allowed():
    """Test that users with dice values other than 1 or 2 cannot use the command"""
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}},
            "active_users": ["@aaa"],
            "cycles": [{"points": {"@aaa": {"message_id": 123, "value": 4}}, "users": ["@aaa"]}],
            "last_play_date": None,
        },
        username="aaa",
        message_value=4,  # Using invalid value (4) - only 1 and 2 are allowed
    )
    await fuck_command(tester.update, tester.context)
    tester.assert_reply_text(
        text="Solo puedes usar este comando si sacaste 1 o 2 en el dado."
    )
    # No changes should be saved to the state