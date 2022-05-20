import discord
from discord.ext import commands
from bot import OWNERS, THEME
from views import ConfirmView

import asyncio
from sqlalchemy.future import select
from uuid import uuid4


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(970283844567728129)
    async def giveaccess(self, ctx: commands.Context):
        author = ctx.author
        role = ctx.guild.get_role(970282638394949653)

        for person in author.guild.members:
            if role not in person.roles and person.bot == False:
                await person.add_roles(role)

        e = discord.Embed(
            title="Access given to all members!",
            description=f"Server access to all members has been given by {ctx.author.mention}!",
        )
        c = self.bot.get_channel(970284928711413790)
        await c.send(embed=e)

    @commands.command()
    @commands.has_role(970283844567728129)
    async def warn(self, ctx: commands.Context):
        ...


def setup(bot):
    bot.add_cog(Staff(bot))
