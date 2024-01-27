import discord
import ezcord
import os

from dotenv import load_dotenv

bot = ezcord.Bot(
    intents=discord.Intents.all(),
    language="de",
    debug_guilds=[1191056685712806011]
)

if __name__ == "__main__":
    bot.load_cogs("source", ignored_cogs="embed tempvoice daily setup", subdirectories=True)
    load_dotenv()
    bot.run(os.getenv("TOKEN"))