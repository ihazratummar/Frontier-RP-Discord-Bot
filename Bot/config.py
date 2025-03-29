import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

exts = {
    "Bot.cogs.verification.verification"
}


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=command_prefix, intents= intents, **kwargs)


    async def on_ready(self):
        for ext in exts:
            if ext not in self.extensions:
                await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Bot is ready.")

        await self.change_presence(
            activity=discord.Activity(
                type = discord.ActivityType.watching,
                            name = "over the server")
        )
            


__all__ = ["Bot, bot_token"]