from asyncio import events
from multiprocessing import Event
import discord
from discord.ext import commands
import os, datetime
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token")

bot = commands.Bot(command_prefix="", help_command=None, intents=discord.Intents.all())

# Suggestions & Feedback
@bot.event
async def on_message(msg):
    if msg.author.id == bot.user.id:
        return
    # Suggestions
    if msg.channel.id == 970301282646650940:
        if msg.author.id != 400857098121904149 or msg.author.id != 702385226407608341:
            return
        await msg.delete()
        e = discord.Embed(title="Suggestion", description=f"{msg.content}", timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")
    # Feedback
    if msg.channel.id == 970282258890096658:
        if msg.author.id != 400857098121904149 or msg.author.id != 702385226407608341:
            return
        e = discord.Embed(title="Feedback", description=f"{msg.content}", timestamp=datetime.datetime.utcnow(), color=discord.Color.embed_background())
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")

@bot.event
async def on_ready():
    print("Online")


bot.run(token)
