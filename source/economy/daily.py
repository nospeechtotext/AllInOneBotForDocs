import discord
import ezcord
import random
from discord.ext import commands
from discord.commands import slash_command
from data import emoji

class EconomyDatabase(ezcord.DBHandler):
    def __init__(self):
        super().__init__("data/db/economy.db")

    async def get_cookies(self, user_id):
        return await self.one("SELECT cookies FROM users WHERE user_id = ?", user_id)

    async def add_cookies(self, user_id, cookies):
        async with self.start() as cursor:
            await cursor.exec("INSERT OR IGNORE INTO users (user_id) VALUES (?)", user_id)
            await cursor.exec("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", cookies, user_id)

db = EconomyDatabase()
class DailyIncome(ezcord.Cog):

    @slash_command(description="Hole deine täglichen Kekse ab.")
    @commands.cooldown(1, 86400)
    async def daily(self, ctx: discord.ApplicationContext):
        income = random.randint(5, 15)

        await db.add_cookies(ctx.user.id, income)
        cookies = await db.get_cookies(ctx.user.id)

        embed = discord.Embed(
            color=emoji.color_blue,
            title="🍪 Tägliche Kekse!",
            description=f"Du hast dir **{income}** 🍪 abgeholt, und hast nun **{cookies}** 🍪"
        )
        await ctx.respond(embed=embed)
def setup(bot: discord.Bot):
    bot.add_cog(DailyIncome(bot))