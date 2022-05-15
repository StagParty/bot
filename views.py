import discord
from discord import ButtonStyle

class ConfirmView(discord.ui.View):
    do_action: bool

    def __init__(self, author_id: int):
        super().__init__()
        self.author_id = author_id

    @discord.ui.button(label="Confirm", style=ButtonStyle.danger)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.author_id == interaction.user.id:
            self.do_action = True
            self.stop()
            await interaction.message.edit(content="Confirming...", view=None)

    @discord.ui.button(label="Cancel", style=ButtonStyle.grey)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.author_id == interaction.user.id:
            self.do_action = False
            self.stop()
            await interaction.message.edit(content="Cancelling...", view=None)