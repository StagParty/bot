import asyncio
import discord
from discord.ext import commands


class ModMail(commands.Cog):
    """
    Cog that handles Mod Mail
    """

    mod_mail_channel = 970561589734416425

    # Key: ID of message sent in mod mail channel
    # Value: Original message sent in bot's DMs
    mail_authors: dict[int, discord.Message] = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handle_mod_reply(self, msg: discord.Message):
        if not (ref := msg.reference):
            return

        if original_msg := self.mail_authors.get(ref.message_id):  # type: ignore
            to_file_tasks = [att.to_file() for att in msg.attachments[:10]]
            files = await asyncio.gather(*to_file_tasks)

            try:
                await original_msg.reply(f"{msg.author.mention}: {msg.content}", files=files)
            except discord.HTTPException or discord.Forbidden as e:
                await msg.reply(f"Unable to send message to user: {e}")

    async def handle_dm_reply(self, msg: discord.Message):
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

        mm_channel: discord.TextChannel = self.bot.get_channel(self.mod_mail_channel) or await self.bot.fetch_channel(self.mod_mail_channel)  # type: ignore

        try:
            mm_msg = await mm_channel.send(
                embed=mm_embed, allowed_mentions=discord.AllowedMentions.none()
            )
            self.mail_authors[mm_msg.id] = msg

        except discord.HTTPException as e:
            await msg.author.send(
                f"Unable to send message: ```{e}```",
                reference=msg.to_reference(),
            )

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        if msg.guild:
            if msg.channel.id == self.mod_mail_channel:
                asyncio.create_task(self.handle_mod_reply(msg))
        else:
            asyncio.create_task(self.handle_dm_reply(msg))


def setup(bot: commands.Bot):
    bot.add_cog(ModMail(bot))
