import discord
import ezcord
import random
from discord.ext import commands
from discord.commands import SlashCommandGroup
from data import emoji
import os
class EconomyDatabase(ezcord.DBHandler):
    def __init__(self):
        super().__init__("data/db/economy.db")

    async def setup(self):
        await self.exec("""
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        cookies INTEGER DEFAULT 0
        )
        """)

    async def get_cookies(self, user_id):
        return await self.one("SELECT cookies FROM users WHERE user_id = ?", user_id)

    async def add_cookies(self, user_id, cookies):
        async with self.start() as cursor:
            await cursor.exec("INSERT OR IGNORE INTO users (user_id) VALUES (?)", user_id)
            await cursor.exec("UPDATE users SET cookies = ? WHERE user_id = ?", cookies, user_id)

db = EconomyDatabase()

class CookieDB(ezcord.Cog):
    db = SlashCommandGroup("db")

    @db.command(description="Löscht alle Daten aus der Datenbank.")
    async def delete(self, ctx):
        await ctx.defer()

        embed = discord.Embed(
            color=0x0198ff,
            title=f"🍪 Keks-Datenbank löschen?",
            description="Möchtest du die **Keks-Datenbank wirklich löschen?**"
        )
        await ctx.respond(embed=embed, view=AcceptDelete(ctx))
def setup(bot: discord.Bot):
    bot.add_cog(CookieDB(bot))

class AcceptDelete(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(timeout=30, disable_on_timeout=True)

    @discord.ui.button(
        label="✅",
        custom_id="Tick"
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        if self.ctx.user.id == interaction.user.id:
            os.remove("data/db/economy.db")

            embed = discord.Embed(
                color=0x0198ff,
                title=f"🍪 Keks-Datenbank gelöscht!",
                description="Die Keks-Datenbank wurde gelöscht! Bitte den Bot neustarten, um Fehler vorzubeugen."
            )
            await interaction.message.edit(embed=embed, view=None)
        else:
            await interaction.response.send_message("> **Du bist nicht berechtigt, die Keks-Datenbank zu löschen!**", ephemeral=True)