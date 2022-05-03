import os
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

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


@bot.event
async def on_ready():
    print("Online")


if __name__ == "__main__":
    bot.load_extension("cogs.modmail")
    bot.load_extension("cogs.utils")
    bot.run(token)
