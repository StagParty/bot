import asyncio
import discord
from discord import utils as discord_utils
from discord.ext import commands


class ModMail(commands.Cog):
    """
    Cog that handles Mod Mail
    """

    mod_mail_channel = 970561589734416425

    # Key: Mail sender's ID
    # Value: Corresponding Discord Thread
    mail_threads: dict[int, discord.Thread] = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handle_mod_reply(self, msg: discord.Message):
        original_author_id = int(msg.channel.name.rsplit(" | ", 1)[-1])  # type: ignore

        if original_author := await self.bot.get_or_fetch_user(
            original_author_id
        ):
            to_file_tasks = [att.to_file() for att in msg.attachments[:10]]
            files = await asyncio.gather(*to_file_tasks)

            try:
                await original_author.send(
                    f"{msg.author.mention}: {msg.content}", files=list(files)
                )
            except discord.HTTPException or discord.Forbidden as e:
                await msg.reply(f"Unable to send message to user: ```{e}```")

    async def handle_dm_reply(self, msg: discord.Message):
        cleaned_content = msg.content.replace("\n", " ")

        mm_embed = discord.Embed(
            description=cleaned_content,
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

        if not (thread := self.mail_threads.get(msg.author.id)):
            # Find the required thread in channel threads, create a new thread if not found
            thread = discord_utils.find(
                lambda t: t.name.endswith(str(msg.author.id)),
                mm_channel.threads,
            ) or await mm_channel.create_thread(
                name=f"{msg.author.name} | {msg.author.id}",
                type=discord.ChannelType.public_thread,
            )
            self.mail_threads[msg.author.id] = thread

        try:
            await thread.send(embed=mm_embed)
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
            if (
                isinstance(msg.channel, discord.Thread)
                and msg.channel.parent_id == self.mod_mail_channel
            ):
                asyncio.create_task(self.handle_mod_reply(msg))
        else:
            asyncio.create_task(self.handle_dm_reply(msg))


def setup(bot: commands.Bot):
    bot.add_cog(ModMail(bot))
