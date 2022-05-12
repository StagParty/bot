import discord
from discord.ext import commands
from bot import OWNERS, THEME
from views import ConfirmView

import asyncio
import db
from db import models
from sqlalchemy.future import select
from uuid import uuid4


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaccess(self, ctx):
        if ctx.author.id in OWNERS:
            author = ctx.author
            role = discord.utils.get(author.guild.roles, id=970282638394949653)

            for person in author.guild.members:
                if role not in person.roles and person.bot == False:
                    await person.add_roles(role)
            e = discord.Embed(title="Access given to all members!", description=f"Server access to all members has been given by {ctx.author.mention}!")
            c = self.bot.get_channel(970284928711413790)
            await c.send(embed=e)
        else:
            await ctx.send("You're not allowed to do this!")

    @commands.slash_command(guild_ids=[970282258890096651])
    @commands.has_guild_permissions(administrator=True)
    async def warn(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        *,
        reason: str,
    ):
        """
        Warn a member for doing something they weren't supposed to
        """

        await ctx.defer()

        if (
            ctx.guild.owner_id != ctx.author.id
            and ctx.author.top_role <= member.top_role
        ):
            await ctx.respond(
                "You cannot use the command on this person because their top role is higher than or equal to yours."
            )
            return

        new_infraction = models.Infraction(
            id=uuid4().hex,
            guild_id=ctx.guild_id,
            user_id=member.id,
            moderator_id=ctx.author.id,
            reason=reason,
        )

        async with db.async_session() as session:
            session.add(new_infraction)
            await session.commit()

        await ctx.respond(f"**{member}** has been warned because: *{reason}*")

    @commands.slash_command(guild_ids=[970282258890096651])
    @commands.has_guild_permissions(administrator=True)
    async def infractions(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member = None,
    ):
        """
        See all the infractions in this server
        """

        async with db.async_session() as session:
            q = select(models.Infraction).where(
                models.Infraction.guild_id == ctx.guild_id
            )

            if member:
                q = q.where(models.Infraction.user_id == member.id)

            result = await session.execute(q)
            infracs: list[models.Infraction] = result.scalars().all()

        if member:
            embed_title = f"Infractions by {member} in {ctx.guild.name}"
        else:
            embed_title = f"All Infractions in {ctx.guild.name}"

        infractions_embed = discord.Embed(title=embed_title, color=THEME)

        if infracs:

            async def embed_task(infraction: models.Infraction):
                if member:
                    guild_member = member
                else:
                    guild_member = await ctx.guild.fetch_member(
                        infraction.user_id
                    )

                moderator = await ctx.guild.fetch_member(
                    infraction.moderator_id
                )

                infractions_embed.add_field(
                    name=f"ID: {infraction.id}",
                    value=(
                        f"**Member:** {guild_member.mention}\n"
                        f"**Reason:** {infraction.reason}\n"
                        f"**Warned by:** {moderator.mention}"
                    ),
                    inline=False,
                )

            tasks = [embed_task(inf) for inf in infracs]
            await asyncio.gather(*tasks)

        elif member:
            infractions_embed.description = (
                f"There are no infractions for {member}"
            )
        else:
            infractions_embed.description = (
                "There are no infractions in this server"
            )

        await ctx.respond(embed=infractions_embed)

    @commands.slash_command(name="clearinfractions", guild_ids=[970282258890096651])
    @commands.has_guild_permissions(administrator=True)
    async def clear_infractions(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member = None,
    ):
        """
        Clear somebody's infractions in the current server
        """

        if member is None:
            confirm_view = ConfirmView(ctx.author.id)
            await ctx.respond(
                "You are about to clear everyone's infractions in this server. Do you want to continue?",
                view=confirm_view,
            )
            await confirm_view.wait()

            if confirm_view.do_action:
                async with db.async_session() as session:
                    q = select(models.Infraction).where(
                        models.Infraction.guild_id == ctx.guild_id
                    )
                    result = await session.execute(q)
                    tasks = [
                        session.delete(inf) for inf in result.scalars().all()
                    ]
                    await asyncio.gather(*tasks)
                    await session.commit()

                await ctx.respond("Cleared all infractions in this server")

        else:
            if (
                ctx.guild.owner_id != ctx.author.id
                and ctx.author.top_role <= member.top_role
            ):
                await ctx.respond(
                    "You cannot use the command on this person because their top role is higher than or equal to yours."
                )
                return

            async with db.async_session() as session:
                q = (
                    select(models.Infraction)
                    .where(models.Infraction.guild_id == ctx.guild_id)
                    .where(models.Infraction.user_id == member.id)
                )
                result = await session.execute(q)
                tasks = [session.delete(inf) for inf in result.scalars().all()]
                await asyncio.gather(*tasks)
                await session.commit()

            await ctx.respond(
                f"Cleared all infractions by **{member}** in this server"
            )

    @commands.slash_command(name="removeinfraction", guild_ids=[970282258890096651])
    @commands.has_guild_permissions(administrator=True)
    async def remove_infraction(
        self, ctx: discord.ApplicationContext, id: str
    ):
        """
        Delete a particular infraction
        """

        async with db.async_session() as session:
            inf = await session.get(models.Infraction, id)

            if inf:
                await session.delete(inf)
                await session.commit()
                await ctx.respond(f"Deleted infraction with ID `{id}`")
            else:
                await ctx.respond("Unable to find an infraction with that ID")

def setup(bot):
    bot.add_cog(Staff(bot))
