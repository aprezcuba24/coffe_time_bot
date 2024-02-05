import pytest
from unittest.mock import AsyncMock, patch
from app.handlers.dice import yes_play_dice_query


@pytest.mark.asyncio
@patch("app.handlers.dice.has_open_game", return_value=True)
async def test_has_open_game(*args):
    assert await yes_play_dice_query(None, None) is None


@pytest.mark.asyncio
@patch("app.handlers.dice.open_game", return_value=["@aaa", "@bbb"])
@patch("app.handlers.dice.has_open_game", return_value=False)
@patch("app.handlers.dice.register_point")
async def test_new_game(register_point_mock, *args):
    update = AsyncMock()
    update.callback_query.data = "dice_yes_play/7525/5"
    context = AsyncMock()
    await yes_play_dice_query(update, context)
    update.effective_message.edit_text.assert_called_once_with(
        text="gogogogogogogogogogogogo \n @aaa @bbb",
    )
    register_point_mock.assert_called_once_with(update, context, 7525, 5)
