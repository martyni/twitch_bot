"""
Twitch chat bot for channel martyn123 using bot account bot123.
Built with TwitchIO (https://github.com/PythonistaGuild/TwitchIO).
"""

import logging
import os
import random

import twitchio
from twitchio import eventsub
from twitchio.authentication import UserTokenPayload
from twitchio.ext import commands

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
LOGGER: logging.Logger = logging.getLogger("TwitchBot")


class Bot(commands.Bot):
    """A simple Twitch chat bot for channel martyn123."""

    def __init__(self) -> None:
        super().__init__(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            bot_id=os.environ["BOT_ID"],
            owner_id=os.environ["BROADCASTER_ID"],
            prefix="!",
        )

    async def setup_hook(self) -> None:
        # Subscribe to chat messages in the broadcaster's channel via EventSub WebSocket.
        payload = eventsub.ChatMessageSubscription(
            broadcaster_user_id=self.owner_id,
            user_id=self.bot_id,
        )
        await self.subscribe_websocket(payload=payload)
        LOGGER.info("Subscribed to chat messages in channel %s", self.owner_id)

    async def event_ready(self) -> None:
        LOGGER.info("Bot is ready! Logged in as %s (ID: %s)", self.nick, self.bot_id)

    async def event_oauth_authorized(self, payload: UserTokenPayload) -> None:
        """Called when a user authorizes the bot via OAuth."""
        LOGGER.info("OAuth token authorized for user ID: %s", payload.user_id)
        await super().event_oauth_authorized(payload)

    @commands.command()
    async def hello(self, ctx: commands.Context) -> None:
        """Greet the user who invoked the command."""
        await ctx.reply(f"Hello {ctx.chatter}! Welcome to the stream!")

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        """List available bot commands."""
        await ctx.reply("Available commands: !hello, !help, !dice")

    @commands.command()
    async def dice(self, ctx: commands.Context) -> None:
        """Roll a six-sided dice."""
        result = random.randint(1, 6)
        await ctx.reply(f"{ctx.chatter} rolled a {result}!")


def main() -> None:
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
