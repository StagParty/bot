import discord
from discord.ext import commands
import datetime

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        e = discord.Embed(title="StagParty Help", 
        description="**Commands:**\n`!release` - Sends information related to our release\n`!help` - A template for people who need help(sends an embed)\n`!apply` - Apply for staff!",
        timestamp=datetime.datetime.now(),
        color=discord.Color.dark_purple())
        e.set_footer(text="StagParty | stagparty.xyz")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Help(bot))
