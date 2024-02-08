from telegram import Update
from telegram.ext import ContextTypes


def start_params(users):
    return {"text": f"gogogogogogogogogogogogo \n {' '.join(users)}"}


def the_winner(user):
    return {"text": f"Tenemos un ganador {user}"}


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


class Chat:
    _instance = None

    @classmethod
    async def get_instance(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if cls._instance is None:
            cls._instance = Chat(update=update, context=context)
            await cls._instance._load_data()
        return cls._instance

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._update = update
        self._context = context
        self._active_username = f"@{self._update.effective_user.username}"

    async def _load_data(self):
        chat = self._update.effective_chat
        chats = await self._context.application.persistence.get_chat_data()
        chat_data = chats[str(chat.id)]
        self._users = chat_data.get("users", {})
        self._active_users = chat_data.get("active_users", [])
        self._cycles = [CycleItem.load(item) for item in chat_data.get("cycles", [])]

    async def save(self):
        chat_data = {
            "users": self._users,
            "active_users": self._active_users,
            "cycles": [item.to_dict() for item in self._cycles],
        }
        await self._context.application.persistence.update_chat_data(
            chat_id=self._update.effective_chat.id, data=chat_data
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
        self._cycles = [CycleItem(self._active_users)]
        return self._active_users

    def is_active_user(self):
        return self._active_username in self._active_users

    def _get_last_cycle(self) -> CycleItem:
        return self._cycles[-1]

    def _user_has_dice(self):
        return self._get_last_cycle().has_dice(self._active_username)

    def user_has_dice(self):
        if not self.has_open_game():
            return False
        return self._user_has_dice()

    def user_can_dice(self):
        return not self._user_has_dice() and self._get_last_cycle().has_user(
            self._active_username
        )

    def register_point(self, message_id=None, value=None):
        if not self.has_open_game():
            return False
        if self._user_has_dice():
            return False
        message_id = (
            message_id if message_id is not None else self._update.effective_message.id
        )
        value = value if value is not None else self._update.message.dice.value
        last_cycle: CycleItem = self._get_last_cycle()
        last_cycle.add_point(self._active_username, message_id, value)

    def is_the_last_user(self):
        return self._get_last_cycle().is_completed()

    def game_over(self):
        if not self.has_open_game():
            return None
        last_cycle: CycleItem = self._get_last_cycle()
        usernames = last_cycle.get_users_by_score()
        if len(usernames) > 1:
            self._cycles.append(CycleItem(users=usernames))
        else:
            user = usernames[0]
            if user not in self._users:
                self._users[user] = {}
            score = self._users[user].get("score", 0)
            self._users[user]["score"] = score + 1
            self._cycles = []
        return usernames


# def add_user(username, chat_data):
#     if username in chat_data["users"] and username in chat_data["active_users"]:
#         return chat_data
#     chat_data["users"][username] = {}
#     chat_data["active_users"] = chat_data["active_users"] + [username]
#     return chat_data


# def remove_user(username, chat_data):
#     chat_data["active_users"] = [
#         item for item in chat_data["active_users"] if item != username
#     ]
#     return chat_data


# async def get_chat_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat = update.effective_chat
#     chats = await context.application.persistence.get_chat_data()
#     chat_data = chats[str(chat.id)]
#     if "users" not in chat_data:
#         chat_data["users"] = {}
#     if "active_users" not in chat_data:
#         chat_data["active_users"] = []
#     if "cycles" not in chat_data:
#         chat_data["cycles"] = []
#     return chat_data


# async def has_open_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_data = await get_chat_item(update, context)
#     return chat_data["cycles"] != []


# async def open_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_data = await get_chat_item(update, context)
#     active_users = chat_data["active_users"]
#     chat_data["cycles"] = [
#         {
#             "users": active_users,
#             "points": {},
#         }
#     ]
#     await context.application.persistence.update_chat_data(
#         chat_id=update.effective_chat.id, data=chat_data
#     )
#     return active_users


# async def is_active_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_data = await get_chat_item(update, context)
#     username = f"@{update.effective_user.username}"
#     return username in chat_data["active_users"]


# async def _user_has_dice(update: Update, cycle):
#     users = [item for item in cycle["points"]]
#     username = f"@{update.effective_user.username}"
#     return username in users


# async def _get_last_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_data = await get_chat_item(update, context)
#     cycles = chat_data["cycles"]
#     return cycles[len(cycles) - 1]


# async def user_has_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not await has_open_game(update, context):
#         return False
#     last_cycle = await _get_last_cycle(update, context)
#     return await _user_has_dice(update, last_cycle)


# async def user_can_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     last_cycle = await _get_last_cycle(update, context)
#     username = f"@{update.effective_user.username}"
#     return (
#         not await _user_has_dice(update, last_cycle) and username in last_cycle["users"]
#     )


# async def register_point(
#     update: Update, context: ContextTypes.DEFAULT_TYPE, message_id=None, value=None
# ):
#     if not await has_open_game(update, context):
#         return False
#     chat_data = await get_chat_item(update, context)
#     cycles = chat_data["cycles"]
#     last_cycle = cycles[len(cycles) - 1]
#     if await _user_has_dice(update, last_cycle):
#         return False
#     username = f"@{update.effective_user.username}"
#     message_id = message_id if message_id is not None else update.effective_message.id
#     value = value if value is not None else update.message.dice.value
#     cycles[len(cycles) - 1]["points"][username] = {
#         "message_id": message_id,
#         "value": value,
#     }
#     chat_data["cycles"] = cycles
#     await context.application.persistence.update_chat_data(
#         chat_id=update.effective_chat.id, data=chat_data
#     )


# def _get_users_by_score(cycle):
#     min_value = 7
#     users = []
#     for key, item in cycle["points"].items():
#         if item["value"] < min_value:
#             users = [(key, item)]
#             min_value = item["value"]
#         elif item["value"] == min_value:
#             users.append((key, item))
#     return [key for key, item in users]


# async def is_the_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     last_cycle = await _get_last_cycle(update, context)
#     print(last_cycle)
#     return len(last_cycle["users"]) == len(last_cycle["points"])


# async def game_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not await has_open_game(update, context):
#         return None
#     chat_data = await get_chat_item(update, context)
#     last_cycle = await _get_last_cycle(update, context)
#     usernames = _get_users_by_score(last_cycle)
#     if len(usernames) > 1:
#         cycles = chat_data["cycles"]
#         cycles.append(
#             {
#                 "users": usernames,
#                 "points": {},
#             }
#         )
#         chat_data["cycles"] = cycles
#     else:
#         user = usernames[0]
#         if user not in chat_data["users"]:
#             chat_data["users"][user] = {}
#         score = chat_data["users"][user].get("score", 0)
#         chat_data["users"][user]["score"] = score + 1
#         chat_data["cycles"] = []
#     await context.application.persistence.update_chat_data(
#         chat_id=update.effective_chat.id, data=chat_data
#     )
#     return usernames
