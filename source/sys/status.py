import discord
import ezcord
import random
import asyncio
import datetime
from discord.ext import commands, tasks
from discord.commands import slash_command
from data import emoji


class StatusChanger(ezcord.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        await self.status_loop.start()

    @tasks.loop(seconds=10)
    async def status_loop(self):
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M")

        await self.bot.change_presence(
            activity=discord.CustomActivity(f"⏱️ Es ist {time} Uhr am {date}!"),
        )
        await asyncio.sleep(6)

        usercount = self.bot.users

        await self.bot.change_presence(
            activity=discord.CustomActivity(f"👥 Ich bin auf {len(self.bot.guilds)} Servern und {len(usercount)} Nutzer nutzen mich!"),
        )
        await asyncio.sleep(6)


def setup(bot: discord.Bot):
    bot.add_cog(StatusChanger(bot))