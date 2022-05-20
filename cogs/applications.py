import discord
from discord.ext import commands
import asyncio
from bot import OWNERS, THEME, MANAGEMENT

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apply(self, ctx):
        perms = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            ctx.author: discord.PermissionOverwrite(view_channel = True)
        }
        guild = ctx.guild

        category = discord.utils.get(guild.categories, id=975357329283362836)
        channel = await guild.create_text_channel(f"{ctx.author.name}│{ctx.author.id}", category=category, overwrites=perms)

        await ctx.reply(f"An applcation channel for you has been created! {channel.mention}")

        e = discord.Embed(title="Staff Application", description="This is StagParty's Interactive Staff Application. I will be interviewing you with a series of questions. When answering, please keep your replies in one message only.", color=THEME)
        firstmsg = await channel.send(embed=e)
        await firstmsg.pin()
        await ctx.channel.purge(limit=1)

        questions = ["1. What is your name?",
                    "2. Which staff role do you want to apply for?",
                    "3. Why do you want to apply for staff?",
                    "4. What timezone are you in (convert to GMT)",
                    "5. What will you bring to the staff team and server?",
                    "6. Why should we accept you?",
                    "7. Are you good at making reasonable/appropriate decisions when it comes to performing moderation actions?",
                    "8. Do you have any previous experience in moderation? If so - specify your position + where it was. (Give details on what your job was)" ,
                    "9. If a user is spamming, what will you do?",
                    "10. If a user is sending nsfw messages, what will you do?",
                    "11. A member in the community begins breaking some minor rules, and you punish them. Them and other well known members begin harassing you and arguing about your decision. What do you do?",
                    "12. A member of the staff team of a higher authority begins to abuse their rank and harass you. How do you react?",
                    "13. How would you describe your personality?",
                    "14. Are you fluent in reading and writing English?", 
                    "15. Anything else you would like to tell about yourself?"]
            
        answers = []
        prev_answer_msg: discord.Message | None = None

        def check(m):
            return m.author == ctx.author and m.channel == channel

        for ques in questions:
            if msg := prev_answer_msg:
                await msg.reply(ques)
            else:
                await channel.send(f"{ques}")
                msg = await channel.send(f"{ctx.author.mention}")
                await msg.delete()

            try:
                prev_answer_msg = await self.bot.wait_for('message', timeout=300, check=check)
                answers.append(prev_answer_msg.content)
            except asyncio.TimeoutError:
                await channel.send('This application has been inactive for a while, closing.')
                await channel.delete()
                return

        answerschannel = self.bot.get_channel(975369052790878248)

        embed = discord.Embed(
            title=f"New Application", description=f"User information:\nName: {ctx.author.name}\nID: {ctx.author.id}\nJoined: <t:{int(ctx.author.joined_at.timestamp())}>", color=discord.Color.dark_purple())
        
        for question, answer in zip(questions, answers):
            embed.add_field(name=question, value=answer, inline=False)
        
        msg = await answerschannel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        await channel.send("Your application has been submitted! This channel will be deleted in 5 seconds.")
        await asyncio.sleep(5)
        await channel.delete()

    @commands.command()
    async def accept(self, ctx, id: int):
        if ctx.author.id in OWNERS or ctx.author.id in MANAGEMENT:
            guild = self.bot.get_guild(970282258890096651)
            user = guild.get_member(id)
            print(user)

            e = discord.Embed(title="Application Accepted!", description=f"Your application has been **ACCEPTED**!\n\nWelcome to the staff team! We'll give you a 7-day trial period. ", color=discord.Color.green())
            await user.send(embed=e)

def setup(bot):
    bot.add_cog(Applications(bot))
