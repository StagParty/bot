import os
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

GUILD = [970282258890096651]
OWNERS = [400857098121904149, 702385226407608341]

load_dotenv()
token = os.getenv("token")

bot = commands.Bot(
    command_prefix="!", help_command=None, intents=discord.Intents.all()
)

# Suggestions & Feedback
@bot.event
async def on_message(msg):
    if msg.author.id == bot.user.id or msg.author.bot is True:
        return
    # Suggestions
    if msg.channel.id == 970301282646650940:
        if (
            msg.author.id != 400857098121904149
            or msg.author.id != 702385226407608341
        ):
            return
        await msg.delete()
        e = discord.Embed(
            title="Suggestion",
            description=f"{msg.content}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.embed_background(),
        )
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")
    # Feedback
    if msg.channel.id == 970282258890096658:
        if (
            msg.author.id != 400857098121904149
            or msg.author.id != 702385226407608341
        ):
            return
        e = discord.Embed(
            title="Feedback",
            description=f"{msg.content}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.embed_background(),
        )
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")

    await bot.process_commands(msg)


@bot.command()
async def update(ctx, *, message):
    if ctx.author.id in OWNERS:
        await ctx.message.delete()
        e = discord.Embed(
            title="Update",
            description=f"{message}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.blue(),
        )
        e.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
        update_channel = bot.get_channel(970282514902052874)
        await update_channel.send(embed=e)
    else:
        await ctx.send("You're not allowed to send an update!")


@bot.command()
async def release(ctx):
    await ctx.message.delete()
    e = discord.Embed(
        title="Hello there,",
        description="We are working hard to get EventsApp released into beta.\n\nWhen it is ready it will be announced in <#970282258890096654>.\n\nKind Regards,\nThe EventsApp Team",
        color=discord.Color.dark_purple(),
        timestamp=datetime.datetime.utcnow(),
    )
    e.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar)
    await ctx.send(embed=e)


@bot.event
async def on_ready():
    print("Online")


if __name__ == "__main__":
    bot.load_extension("cogs.modmail")
    bot.run(token)
