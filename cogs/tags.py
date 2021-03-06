import discord
from discord.ext import commands
import datetime


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def release(self, ctx):
        await ctx.message.delete()
        tag_embed = discord.Embed(
            title="Hello there,",
            description="We are working hard to get StagParty released into beta.\n\nWhen it is ready it will be announced in <#970282258890096654>.\n\nKind Regards,\nThe StagParty Team",
            color=discord.Color.dark_purple(),
            timestamp=datetime.datetime.utcnow(),
        )
        tag_embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
        await ctx.send(embed=tag_embed)

    @commands.command()
    async def needhelp(self, ctx):
        await ctx.message.delete()
        tag_embed = discord.Embed(
            title="Need Help?",
            description="Do you need help? Shoot a DM to <@970304297382313984> and we'll reply as fast as we can.\n\nKind Regards,\nThe StagParty Team",
            color=discord.Color.dark_purple(),
            timestamp=datetime.datetime.utcnow(),
        )
        tag_embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
        await ctx.send(embed=tag_embed)


def setup(bot):
    bot.add_cog(Tags(bot))
