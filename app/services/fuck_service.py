import random
from typing import List, Tuple, Dict, Any, Optional

from telegram import Update


class FuckService:
    """Service for handling 'fuck' command functionality."""

    @staticmethod
    def get_users_to_trigger(
        current_username: str,
        users_data: Dict[str, Dict[str, Any]],
        current_dice_value: int,
    ) -> List[str]:
        """
        Get the list of users who have an active fuck command that should be triggered.

        Args:
            current_username: Username of the current user
            users_data: Dictionary of user data
            current_dice_value: Current dice value

        Returns:
            List of usernames that have active fuck commands that should be triggered
        """
        fuck_users = []
        for username, user_data in users_data.items():
            # Skip if this is the current user
            if username == current_username:
                continue

            # Skip if the user doesn't have an active fuck command
            if not user_data.get("fuck_active", False):
                continue

            # Check if the current dice value triggers this user's fuck command
            if current_dice_value <= user_data.get("fuck_value", 6):
                fuck_users.append(username)

        return fuck_users

    @staticmethod
    def get_random_reaction() -> Tuple[str, str]:
        """
        Get a random emoji and reaction message.

        Returns:
            Tuple of (emoji, reaction_message)
        """
        emojis = ["💩", "🖕", "🤡", "👹", "💀", "😈", "🤬", "🔪", "👺", "🤮"]
        emoji = random.choice(emojis)

        reactions = [
            "¡Te jodieron!",
            "¡Alguien te ha dado una maldición!",
            "¡Qué mal número, te han jodido!",
            "¡Alguien está feliz de verte sufrir!",
            "¡Mala suerte, te han maldecido!",
        ]
        reaction = random.choice(reactions)

        return emoji, reaction

    @staticmethod
    def deactivate_fuck_commands(
        users_data: Dict[str, Dict[str, Any]], usernames: List[str]
    ) -> None:
        """
        Deactivate fuck commands for the specified users.

        Args:
            users_data: Dictionary of user data
            usernames: List of usernames to deactivate fuck commands for
        """
        for username in usernames:
            if username in users_data:
                users_data[username]["fuck_active"] = False

    @staticmethod
    def get_angry_emotes() -> Tuple[str, str]:
        """
        Get random angry emojis and symbols for users who have lost.

        Returns:
            Tuple of (emojis, symbol)
        """
        angry_emojis = ["💢", "🤬", "😡", "👿", "😤", "😠", "💥", "🔥", "👹", "👺"]
        angry_symbols = [
            "grrrr",
            "argh",
            "maldición",
            "!!!!",
            "@#$%&!",
            "¡¡¡$#@!!!",
            "ufff",
        ]

        emojis = " ".join(random.sample(angry_emojis, k=min(3, len(angry_emojis))))
        symbol = random.choice(angry_symbols)

        return emojis, symbol

    @staticmethod
    def is_valid_dice_value(dice_value: int) -> bool:
        """
        Check if the dice value is valid for using the fuck command.

        Args:
            dice_value: Dice value to check

        Returns:
            True if the dice value is valid (1 or 2), False otherwise
        """
        return dice_value in [1, 2]

    @staticmethod
    async def process_fuck_triggers(
        update: Update,
        users_data: Dict[str, Dict[str, Any]],
        current_username: str,
        current_dice_value: int,
    ) -> None:
        """
        Process triggers for fuck commands.

        Args:
            update: Telegram update
            users_data: Dictionary of user data
            current_username: Username of the current user
            current_dice_value: Current dice value
        """
        fuck_users = FuckService.get_users_to_trigger(
            current_username, users_data, current_dice_value
        )

        if not fuck_users:
            return

        emoji, reaction = FuckService.get_random_reaction()

        # Deactivate the fuck commands
        FuckService.deactivate_fuck_commands(users_data, fuck_users)

        # Send the message
        await update.effective_message.reply_text(
            text=f"{reaction} {emoji} {' '.join(fuck_users)} está disfrutando tu infortunio."
        )
