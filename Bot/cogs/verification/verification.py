import discord
from discord.ext import commands
from Bot.core.constants import  Color
from Bot.cogs.verification.verification_buttons import NickNameVerificationView

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.hybrid_command(name="verify")
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx: commands.Context):
        """Create the verification and request the member to verify ticket."""
        await ctx.defer()

        embed = discord.Embed(
            title="Запрос на получение роли",
            description="""Нажмите кнопку ниже, чтобы начать процесс подтверждения вашей роли. 😊""",
            color= discord.Color.from_str(Color.brand_color)
        )

        view = NickNameVerificationView()
        await ctx.send(embed=embed, view=view)



async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot=bot))
    bot.add_view(NickNameVerificationView())
