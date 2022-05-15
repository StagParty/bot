import discord
from discord.ext import commands
import asyncio
from bot import THEME

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apply(self, ctx):
        try:
            guild = ctx.guild

            category = discord.utils.get(guild.categories, id=975357329283362836)
            channel = await guild.create_text_channel(f"{ctx.author.name}│{ctx.author.id}", category=category)

            e = discord.Embed(title="Staff Application", description="This is StagParty's Interactive Staff Application. I will be interviewing you with a series of questions. When answering, please keep your replies in one message only.", color=THEME)
            await channel.send(embed=e)

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
                        "16. How would you describe your personality?",
                        "17. Are you fluent in reading and writing English?", 
                        "18. Anything else you would like to tell about yourself?"]
            
            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == channel

            for i in questions:
                await channel.send(i)
                msg = await channel.send(f"{ctx.author.mention}")
                await msg.delete()
                try:
                    msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await channel.send('This application has been inactive for a while, closing.')
                    await channel.delete()
                    return
                else:
                    answers.append(msg.content)

            discordname = answers[0]

            whichstaffrole = answers[1]

            why = answers[2]

            timezone = answers[3]

            whatwillubring = answers[4]

            whyaccept = answers[5]

            reasonabledesicion = answers[6]

            previousstaff = answers[7]

            spamm = answers[8]

            nsfw = answers[9]

            hatingonufordecision = answers[10]

            staffabuse = answers[11]

            personality = answers[12]

            fluent = answers[13]

            anythingelse = answers[14]

            answerschannel = self.bot.get_channel(975369052790878248)

            embed = discord.Embed(
                title=f"New Application", description=f"User information:\nName: {ctx.author.name}\nID: {ctx.author.id}\nJoined: <t:{int(ctx.author.joined_at.timestamp())}>", color=discord.Color.dark_purple())
            embed.add_field(name="Name:", value=f"{discordname}", inline=False)
            embed.add_field(name="Which staff role:", value=f"{whichstaffrole}", inline=False)
            embed.add_field(name="Why do you want to apply:", value=f"{why}", inline=False)
            embed.add_field(name="What is your timezone:",
                            value=f"{timezone}", inline=False)
            embed.add_field(name="What will you bring to the staff team:",
                            value=f"{whatwillubring}", inline=False)
            embed.add_field(name="Why should we accept:", value=f"{whyaccept}", inline=False)
            embed.add_field(name="Can you make reasonable decisions:", value=f"{reasonabledesicion}", inline=False)
            embed.add_field(name="Any previous staff experience:", value=f"{previousstaff}", inline=False)
            embed.add_field(name="If a user is spamming, what will you do:", value=f"{spamm}", inline=False)
            embed.add_field(name="User sending NSFW messages, what will you do", value=f"{nsfw}", inline=False)
            embed.add_field(name="A member in the community begins breaking some minor rules, and you punish them. Them and other well known members begin harassing you and arguing about your decision. What do you do?", value=f"{hatingonufordecision}", inline=False)
            embed.add_field(name="A member of the staff team of a higher authority begins to abuse their rank and harass you. How do you react?", value=f"{staffabuse}", inline=False)
            embed.add_field(name="How will you describe your personality", value=f"{personality}", inline=False)
            embed.add_field(name="Are you fluent:", value=f"{fluent}", inline=False)
            embed.add_field(name="Anything else:", value=f"{anythingelse}", inline=False)
        
            msg = await answerschannel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            await channel.send("Your application has been submitted! This channel will be deleted in 5 seconds.")
            await asyncio.sleep(5)
            await channel.delete()
        except:
            await ctx.respond("I was unable to create a channel for your application!")

def setup(bot):
    bot.add_cog(Applications(bot))
