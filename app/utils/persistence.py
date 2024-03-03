import json
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional, Tuple

from telegram.ext import BasePersistence, PersistenceInput

from app.services.persistence_data import get_persistence_data, save_data


class DynamodbPersistence(BasePersistence):
    """Using dynamodb to make the bot persistent"""

    def __init__(
        self,
        store_data: Optional[PersistenceInput] = None,
        on_flush: bool = False,
        update_interval: float = 60,
    ):
        super().__init__(store_data=store_data, update_interval=update_interval)
        self.on_flush = on_flush
        self.user_data: Optional[DefaultDict[int, Dict]] = None
        self.chat_data: Optional[DefaultDict[int, Dict]] = None
        self.bot_data: Optional[Dict] = None
        self.conversations: Optional[Dict[str, Dict[Tuple, Any]]] = None

    async def load_data(self) -> None:
        data = await get_persistence_data()
        if data:
            self.user_data = defaultdict(dict, json.loads(data["user_data"]))
            self.chat_data = defaultdict(dict, json.loads(data["chat_data"]))
            # For backwards compatibility with files not containing bot data
            self.bot_data = json.loads(data["bot_data"])
            self.conversations = json.loads(data["conversations"])
            self.callback_data = json.loads(data["callback_data"])
        else:
            self.callback_data = dict()
            self.conversations = dict()
            self.user_data = defaultdict(dict)
            self.chat_data = defaultdict(dict)
            self.bot_data = {}

    async def dump_data(self) -> None:
        return await save_data(
            {
                "conversations": json.dumps(self.conversations),
                "user_data": json.dumps(self.user_data),
                "chat_data": json.dumps(self.chat_data),
                "bot_data": json.dumps(self.bot_data),
                "callback_data": json.dumps(self.callback_data),
            }
        )

    async def get_user_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.user_data:
            pass
        else:
            await self.load_data()
        return deepcopy(self.user_data)  # type: ignore[arg-type]

    async def get_chat_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.chat_data:
            pass
        else:
            await self.load_data()
        return deepcopy(self.chat_data)  # type: ignore[arg-type]

    async def get_bot_data(self) -> Dict[Any, Any]:
        if self.bot_data:
            pass
        else:
            await self.load_data()
        return deepcopy(self.bot_data)  # type: ignore[arg-type]

    async def get_conversations(self, name: str) -> Dict:
        if self.conversations:
            pass
        else:
            await self.load_data()
        data = self.conversations.get(name, {}).copy()  # type: ignore[union-attr]
        result = {}
        for key, value in data.items():
            new_key = key.split("|")
            new_key = (int(new_key[0]), int(new_key[1]))
            result[new_key] = value
        return result

    async def update_conversation(
        self, name: str, key: Tuple[int, ...], new_state: Optional[object]
    ) -> None:
        new_key = f"{key[0]}|{key[1]}"
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(new_key) == new_state:
            return
        self.conversations[name][new_key] = new_state
        if not self.on_flush:
            await self.dump_data()

    async def update_user_data(self, user_id: int, data: Dict) -> None:
        if not data:
            return
        item_id = str(user_id)
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(item_id) == data:
            return
        self.user_data[item_id] = data
        if not self.on_flush:
            await self.dump_data()

    async def update_chat_data(self, chat_id: int, data: Dict) -> None:
        item_id = str(chat_id)
        if not data:
            return
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        self.chat_data[item_id] = data
        if not self.on_flush:
            await self.dump_data()

    async def update_bot_data(self, data: Dict) -> None:
        if not data:
            return
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            await self.dump_data()

    async def flush(self) -> None:
        await self.dump_data()

    async def refresh_user_data(self, user_id: int, user_data: Dict) -> None:
        """Does nothing.

        .. versionadded:: 13.6
        .. seealso:: :meth:`telegram.ext.BasePersistence.refresh_user_data`
        """

    async def refresh_chat_data(self, chat_id: int, chat_data: Dict) -> None:
        """Does nothing.

        .. versionadded:: 13.6
        .. seealso:: :meth:`telegram.ext.BasePersistence.refresh_chat_data`
        """

    async def refresh_bot_data(self, bot_data: Dict) -> None:
        """Does nothing.

        .. versionadded:: 13.6
        .. seealso:: :meth:`telegram.ext.BasePersistence.refresh_bot_data`
        """

    async def drop_chat_data(self, chat_id: int) -> None:
        if self.chat_data is None:
            return
        self.chat_data.pop(chat_id, None)

        if not self.on_flush:
            await self.dump_data()

    async def drop_user_data(self, user_id: int) -> None:
        if self.user_data is None:
            return
        self.user_data.pop(user_id, None)

        if not self.on_flush:
            await self.dump_data()

    async def get_callback_data(self) -> Optional[Dict]:
        if self.callback_data:
            pass
        else:
            await self.load_data()
        return deepcopy(self.callback_data)

    async def update_callback_data(self, data: Dict) -> None:
        if not data:
            return
        if self.callback_data == data:
            return
        self.callback_data = data
        if not self.on_flush:
            await self.dump_data()
