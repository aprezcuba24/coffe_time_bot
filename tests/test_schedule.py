import datetime
import json
from unittest.mock import patch

import pytest

from app.schedule import main


def get_data(time="2024-03-01T14:30:00Z"):
    return {
        "version": "0",
        "id": "510fd000-31f2-7259-86bb-33e8ac2e5609",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "474347890914",
        "time": time,
        "region": "us-east-1",
        "resources": [
            "arn:aws:events:us-east-1:474347890914:rule/coffee-time-bot-renier-ScheduleEventsRuleSchedule2-4I2zZhQlDp2X"
        ],
        "detail": {},
    }


def get_persisted_data(last_play_date=None):
    return {
        "chat_data": json.dumps(
            {
                "-1001215010172": {
                    "last_play_date": last_play_date,
                    "users": {"@renierricardo": {}},
                    "active_users": ["@renierricardo"],
                    "cycles": [],
                }
            }
        ),
        "user_data": "{}",
        "persistence_id": "TELEGRAM_CHAT_DATA",
        "bot_data": "{}",
        "conversations": "{}",
        "callback_data": "{}",
    }


@pytest.mark.asyncio
@patch("app.schedule.get_persistence_data", return_value=None)
async def test_no_chat_data(*args):
    data = await main(get_data())
    assert data["body"] == "no_chat"


@pytest.mark.asyncio
@patch(
    "app.schedule.get_persistence_data",
    return_value=get_persisted_data("2024-03-03T18:40"),
)
@patch("app.schedule.open_game_by_schedule")
async def test_not_called_today(open_game_by_schedule, *args):
    await main(get_data("2024-03-02T18:30:00Z"))
    open_game_by_schedule.assert_called_once()


@pytest.mark.asyncio
@patch(
    "app.schedule.get_persistence_data",
    return_value=get_persisted_data("2024-03-03T18:40"),
)
@patch("app.schedule.open_game_by_schedule")
async def test_not_called_in_the_afternoon(open_game_by_schedule, *args):
    await main(get_data("2024-03-03T14:30:00Z"))
    open_game_by_schedule.assert_called_once()


@pytest.mark.asyncio
@patch(
    "app.schedule.get_persistence_data",
    return_value=get_persisted_data("2024-03-03T14:40"),
)
@patch("app.schedule.open_game_by_schedule")
async def test_was_already_called_in_the_morning(open_game_by_schedule, *args):
    await main(get_data("2024-03-03T15:30:00Z"))
    open_game_by_schedule.assert_not_called()


@pytest.mark.asyncio
@patch(
    "app.schedule.get_persistence_data",
    return_value=get_persisted_data("2024-03-03T18:40"),
)
@patch("app.schedule.open_game_by_schedule")
async def test_was_already_called_in_the_afternoon(open_game_by_schedule, *args):
    await main(get_data("2024-03-03T19:30:00Z"))
    open_game_by_schedule.assert_not_called()
