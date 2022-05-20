import json
import os
import datetime
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv

OWNERS = [400857098121904149, 702385226407608341]
DEVELOPERS = [656021685203501066]
GUILD_IDS = [970282258890096651]
MANAGEMENT = [410852168414003200]
THEME = discord.Color.dark_purple()
load_dotenv()
token = os.getenv("token")

bot = commands.Bot(
    command_prefix="!", help_command=None, intents=discord.Intents.all()
)

guild = None
member_role = None
staff_role = None
gfx_role = None
sponsor_role = None
roles_removed_role = None
roles_removed_channel = None

@bot.event  # Suggestions & Feedback
async def on_message(msg):
    if msg.author.id == bot.user.id or msg.author.bot:  # type: ignore
        return
    cleaned_content = msg.content.replace("\n", " ")

    if len(msg.content) > 1000:
        await msg.channel.send("You can only send upto 1000 characters at a time!")
        return

    # Suggestions
    if msg.channel.id == 970301282646650940:
        if (
            msg.author.id == 400857098121904149
            or msg.author.id == 702385226407608341
        ):
            return
        await msg.delete()
        e = discord.Embed(
            title="Suggestion",
            description=f"{cleaned_content}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.embed_background(),
        )
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")
        await msg.delete()
    # Feedback
    if msg.channel.id == 970282258890096658:
        if (
            msg.author.id == 400857098121904149
            or msg.author.id == 702385226407608341
        ):
            return
        e = discord.Embed(
            title="Feedback",
            description=f"{cleaned_content}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.embed_background(),
        )
        e.set_author(name=f"{msg.author}", icon_url=f"{msg.author.avatar}")
        msgsent = await msg.channel.send(embed=e)
        await msgsent.add_reaction("✅")
        await msgsent.add_reaction("❌")
        await msg.delete()
    await bot.process_commands(msg)

@bot.event
async def on_ready():
    print("Online")
    global guild
    global member_role
    global staff_role
    global gfx_role
    global sponsor_role
    global roles_removed_role
    global roles_removed_channel
    guild = bot.get_guild(970282258890096651)
    member_role = guild.get_role(970282638394949653)
    staff_role = guild.get_role(975351629916307496)
    gfx_role = guild.get_role(973594405770506351)
    sponsor_role = guild.get_role(973589989512319046)
    roles_removed_role = guild.get_role(976145824755101776)
    roles_removed_channel = bot.get_channel(976145984096714892)

@bot.event
async def on_presence_update(before, after):
    if after.bot == True:
        return
    if after.id == 702385226407608341 or after.id == 400857098121904149:
        return
    for activity in after.activities:
        if isinstance(activity, discord.CustomActivity):
            if activity.name.startswith("https://") or "discord.gg/" in activity.name or ".gg/" in activity.name:
                if "https://stagparty.xyz" in activity.name:
                    await after.remove_roles(roles_removed_role)
                    with open("roles.json") as f:
                        dict = json.load(f)
                        values = dict[str(after.id)]
                        for i in range(len(values)):
                            roleid = values[i]
                            role = guild.get_role(roleid)
                            await after.add_roles(role)
                        values.clear()
                    with open("roles.json", 'w') as f:
                        json.dump(dict, f)
                    return
                with open("roles.json", 'r') as f:
                    loader = json.load(f)
                loader[str(after.id)] = []
                time.sleep(1)
                await after.add_roles(roles_removed_role)
                if member_role in after.roles:
                    loader[str(after.id)].append(970282638394949653)
                    await after.remove_roles(member_role)
                if staff_role in after.roles:
                    loader[str(after.id)].append(975351629916307496)
                    await after.remove_roles(staff_role)
                if gfx_role in after.roles:
                    loader[str(after.id)].append(973594405770506351)
                    await after.remove_roles(gfx_role)
                if sponsor_role in after.roles:
                    loader[str(after.id)].append(973589989512319046)
                    await after.remove_roles(sponsor_role)
                with open("roles.json", 'w') as f:
                    json.dump(loader, f)
                msg = await roles_removed_channel.send(str(after.mention))
                await msg.delete()
            else:
                await after.remove_roles(roles_removed_role)
                with open("roles.json") as f:
                    dict = json.load(f)
                    values = dict[str(after.id)]
                    for i in range(len(values)):
                        roleid = values[i]
                        role = guild.get_role(roleid)
                        await after.add_roles(role)
                    values.clear()
                with open("roles.json", 'w') as f:
                    json.dump(dict, f)

if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(token)
