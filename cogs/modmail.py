import discord
from discord.ext import commands


class ModMail(commands.Cog):
    """
    Cog that handles Mod Mail
    """

    mod_mail_channel = 970561589734416425

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # Ensure message is in DMs
        if msg.guild:
            return

        cleaned_content = msg.content.replace("\n", " ")
        timestamp_str = f"Sent on <t:{int(msg.created_at.timestamp())}>"

        mm_embed = discord.Embed(
            description=f"{cleaned_content}\n\n**{timestamp_str}**",
            color=discord.Color.random(),
        )
        mm_embed.set_author(
            name=str(msg.author), icon_url=msg.author.display_avatar.url
        )

        # Attachment previews
        attachment_count = len(msg.attachments)
        if attachment_count > 0:
            mm_embed.set_image(url=msg.attachments[0].url)
        if attachment_count > 1:
            mm_embed.set_thumbnail(url=msg.attachments[1].url)

        # Attachment links
        if msg.attachments:
            attachments_str_list = [
                f"[{att.filename}]({att.url})" for att in msg.attachments
            ]
            attachments_str = "\n".join(attachments_str_list)
            mm_embed.add_field(name="All Attachments", value=attachments_str)

        mm_channel: discord.TextChannel = await self.bot.fetch_channel(self.mod_mail_channel)  # type: ignore

        try:
            await mm_channel.send(
                embed=mm_embed, allowed_mentions=discord.AllowedMentions.none()
            )
        except discord.HTTPException as e:
            await msg.author.send(
                f"Unable to send message: ```{e.text}```",
                reference=msg.to_reference(),
            )


def setup(bot: commands.Bot):
    bot.add_cog(ModMail(bot))
