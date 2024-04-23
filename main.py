import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands

# Import the Cogs
from modules.meme import Meme
from modules.tech_news import TechNews
from modules.support import Support
from modules.future import FuturePlans

load_dotenv()
token = os.getenv("BOT_TOKEN")
owner_id = os.getenv("OWNER_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents, owner_id=owner_id)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="memes and tech news"
        )
    )
    await bot.add_cog(Meme(bot))
    await bot.add_cog(TechNews(bot))
    await bot.add_cog(Support(bot))
    await bot.add_cog(FuturePlans(bot))

    slash_cmd = await bot.tree.sync()

    print(
        "{0} is ready! Synced {1} slash commands".format(bot.user.name, len(slash_cmd))
    )


bot.run(token=token)
