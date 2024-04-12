import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands

# Import the Cogs
from modules.meme import Meme
from modules.tech_news import TechNews
from modules.feedback import Feedback

load_dotenv()
token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents, owner_id=889091852555395122)
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
    await bot.add_cog(Feedback(bot))

    slash_cmd = await bot.tree.sync()

    print(
        "{0} is ready! Synced {1} slash commands".format(bot.user.name, len(slash_cmd))
    )


@bot.command()
async def help(ctx):
    embedVar = discord.Embed(
        title="May-May Wala Aagaya!",
        description="I send memes and important tech news that the masters of this server have selected. You can find the list of all my commands below: -",
        color=0x00FF00,
    )
    allCogs = bot.cogs
    for cog in allCogs:
        commands = bot.get_cog(cog).get_commands()
        cog_commands = ""
        for command in commands:
            cog_commands += f"**{command.name}** - {command.brief}\n"
        embedVar.add_field(name=f"**__{cog}__**\n\n", value=cog_commands, inline=False)
    await ctx.send(embed=embedVar)


bot.run(token=token)
