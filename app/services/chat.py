from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes


async def user_not_active(update):
    return await update.effective_message.reply_text(
        text="Tu usuario no está activo. Adiciónalo primero."
    )


def start_params(users):
    return {"text": f"gogogogogogogogogogogogo \n {' '.join(users)}"}


async def game_over_message(users, update: Update):
    if len(users) == 1:
        return await update.get_bot().send_message(
            chat_id=update.effective_chat.id, text=f"Tenemos un ganador {users[0]}"
        )
    return await update.get_bot().send_message(
        chat_id=update.effective_chat.id, text=f"Desempate {' '.join(users)}"
    )


class CycleItem:
    def __init__(self, users, points=None):
        self._users = users
        self._points = {} if points is None else points

    @classmethod
    def load(cls, data):
        users = data["users"]
        points = data.get("points", {})
        return CycleItem(users=users, points=points)

    def to_dict(self):
        return {
            "users": self._users,
            "points": self._points,
        }

    def has_dice(self, username):
        return username in self._points

    def has_user(self, username):
        return username in self._users

    def add_point(self, username, message_id, value):
        self._points[username] = {
            "message_id": message_id,
            "value": value,
        }

    def get_users_by_score(self):
        min_value = 7
        users = []
        for key, item in self._points.items():
            if item["value"] < min_value:
                users = [key]
                min_value = item["value"]
            elif item["value"] == min_value:
                users.append(key)
        return users

    def is_completed(self):
        return len(self._users) == len(self._points)


class ChatItem:
    def __init__(self, chat_id, persistence):
        self.chat_id = chat_id
        self.persistence = persistence

    @property
    def active_users(self):
        return self._active_users

    def load_data(self, chat_data):
        last_play_date = chat_data.get("last_play_date")
        self._last_play_date = (
            datetime.fromisoformat(last_play_date) if last_play_date else None
        )
        self._users = chat_data.get("users", {})
        self._active_users = chat_data.get("active_users", [])
        self._cycles = [CycleItem.load(item) for item in chat_data.get("cycles", [])]

    @property
    def last_play_date(self):
        return self._last_play_date

    def to_dict(self):
        return {
            "last_play_date": (
                self._last_play_date.isoformat(timespec="minutes")
                if self._last_play_date
                else None
            ),
            "users": self._users,
            "active_users": self._active_users,
            "cycles": [item.to_dict() for item in self._cycles],
        }

    async def save(self):
        await self.persistence.update_chat_data(
            chat_id=self.chat_id, data=self.to_dict()
        )

    def add_user(self, username):
        if username not in self._users:
            self._users[username] = {}
        if username not in self._active_users:
            self._active_users.append(username)

    def remove_user(self, username):
        self._active_users = [item for item in self._active_users if item != username]

    def has_open_game(self):
        return self._cycles != []

    def open_game(self):
        self._last_play_date = datetime.now()
        self._cycles = [CycleItem(self._active_users)]
        return self._active_users

    def _get_last_cycle(self) -> CycleItem:
        return self._cycles[-1]

    def user_has_dice(self):
        if not self.has_open_game():
            return False
        return self._user_has_dice()

    def is_the_last_user(self):
        return self._get_last_cycle().is_completed()

    def game_over(self):
        if not self.has_open_game():
            return None
        last_cycle: CycleItem = self._get_last_cycle()
        usernames = last_cycle.get_users_by_score()
        if len(usernames) == 0:
            self._cycles = []
        elif len(usernames) > 1:
            self._cycles.append(CycleItem(users=usernames))
        else:
            user = usernames[0]
            if user not in self._users:
                self._users[user] = {}
            score = self._users[user].get("score", 0)
            self._users[user]["score"] = score + 1
            self._cycles = []
        return usernames


class Chat(ChatItem):
    @classmethod
    async def get_instance(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        instance = Chat(update=update, context=context)
        chat = update.effective_chat
        chats = await context.application.persistence.get_chat_data()
        chat_data = chats[str(chat.id)]
        instance.load_data(chat_data)
        return instance

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        super().__init__(
            update.effective_chat.id,
            context.application.persistence,
        )
        self._active_username = f"@{update.effective_user.username}"
        self.message_id = update.effective_message.id
        self.dice_value = update.message.dice.value if update.message.dice else 0
        self._update = update
        self._context = context

    def register_point(self, message_id=None, value=None):
        if not self.has_open_game():
            return False
        if self._user_has_dice():
            return False
        message_id = message_id if message_id is not None else self.message_id
        value = value if value is not None else self.dice_value
        last_cycle: CycleItem = self._get_last_cycle()
        last_cycle.add_point(self._active_username, message_id, value)

    def is_active_user(self):
        return self._active_username in self._active_users

    def _user_has_dice(self):
        return self._get_last_cycle().has_dice(self._active_username)

    def user_can_dice(self):
        return not self._user_has_dice() and self._get_last_cycle().has_user(
            self._active_username
        )
