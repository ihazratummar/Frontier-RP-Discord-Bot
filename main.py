from Bot.config import Bot, bot_token
import discord

if __name__ == "__main__":
    bot = Bot(command_prefix="f!", intents= discord.Intents.all(), help_command=None)
    bot.run(bot_token)