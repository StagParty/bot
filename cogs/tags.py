import discord
from discord.ext import commands


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def release(self, ctx):
        await ctx.message.delete()
        e = discord.Embed(
            title="Hello there,",
            description="We are working hard to get EventsApp released into beta.\n\nWhen it is ready it will be announced in <#970282258890096654>.\n\nKind Regards,\nThe EventsApp Team",
            color=discord.Color.dark_purple(),
            timestamp=datetime.datetime.utcnow(),
        )
        e.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
        await ctx.send(embed=e)

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        e = discord.Embed(
            title="Need Help?",
            description="Do you need help? Shoot a DM to <@970304297382313984> and we'll reply as fast as we can.\n\nKind Regards,\nThe EventsApp Team",
            color=discord.Color.dark_purple(),
            timestamp=datetime.datetime.utcnow(),
        )
        e.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Tags(bot))
