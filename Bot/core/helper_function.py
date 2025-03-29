import discord
from Bot.core.constants import Channel
import time

async def send_log(title:str, description: str, guild: discord.Guild, color: discord.Color):

    log_channel = guild.get_channel(Channel.nickname_logs)

    t = time.localtime()
    formatted_time = time.strftime("%y-%m-%d %H:%M:%S", t)

    embed = discord.Embed(
        title= title,
        description= description, 
        color= color
    )
    embed.add_field(name="Time", value=formatted_time)
    await log_channel.send(embed=embed)
