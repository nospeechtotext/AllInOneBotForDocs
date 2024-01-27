import discord
import ezcord
import random

from discord import Interaction
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from data import emoji


class Embed(ezcord.Cog):
    embed = SlashCommandGroup("embed")

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(EmbedEditor(title=None, description=None))

    @embed.command(description="Erstellt ein Embed.")
    async def create(self, ctx: discord.ApplicationContext):
        title = "Dein Titel"
        description = "Deine Beschreibung"
        embed = discord.Embed(
            title=title,
            description=description
        )
        await ctx.respond(embed=embed, view=EmbedEditor(title=title, description=description))

def setup(bot: discord.Bot):
    bot.add_cog(Embed(bot))

class EmbedTitleEditModal(discord.ui.Modal):
    def __init__(self, description, *args, **kwargs):
        self.description = description
        super().__init__(
            discord.ui.InputText(
                label="Embed Titel",
                placeholder="Gebe hier den Embed Titel ein!"
            ),
            *args,
            **kwargs
        )
    async def callback(self, interaction: Interaction):
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.description
        )
        await interaction.message.edit(embed=embed)

class EmbedDescriptionEditModal(discord.ui.Modal):
    def __init__(self, title1, description, *args, **kwargs):
        self.title1 = title1
        self.description = description
        super().__init__(
            discord.ui.InputText(
                label="Embed Description",
                placeholder="Gebe hier die Embed Description ein!"
            ),
            *args,
            **kwargs
        )
    async def callback(self, interaction: Interaction):
        embed = discord.Embed(
            title=self.title1,
            description=self.children[0].value
        )
        await interaction.message.edit(embed=embed)

class EmbedEditor(discord.ui.View):
    def __init__(self, title, description):
        self.title = title
        self.description = description
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Titel bearbeiten", emoji="1️⃣"),
        discord.SelectOption(label="Description bearbeiten", emoji="2️⃣")
    ]

    @discord.ui.select(
        placeholder="Triff eine Auswahl",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="CoolerSelect"
    )
    async def edit_title_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Titel bearbeiten":
            await interaction.response.send_modal(EmbedTitleEditModal(title="Titel bearbeiten", description=self.description))
        else:
            await interaction.response.send_modal(EmbedDescriptionEditModal(title="Description bearbeiten", title1=self.title, description=self.description))