import discord
from discord.ext import commands
import datetime
from bot import OWNERS


class Utils(commands.Cog):
    """
    Utility cog for the bot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update(self, ctx, *, message):
        if ctx.author.id in OWNERS:
            await ctx.message.delete()
            e = discord.Embed(
                title="Update",
                description=f"{message}",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue(),
            )
            e.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
            update_channel = self.bot.get_channel(970282514902052874)
            await update_channel.send(embed=e)
        else:
            await ctx.send("You're not allowed to send an update!")

def setup(bot):
    bot.add_cog(Utils(bot))
