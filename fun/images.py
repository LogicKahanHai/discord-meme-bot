import discord
from discord.ext import commands
from discord import app_commands
import requests

class ImageCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="dog",
        description="Get a random dog image",
    )
    async def dog(self, interaction: discord.Interaction):
        try:
            response = requests.get("https://api.thedogapi.com/v1/images/search")
            data = response.json()
            image_url = data[0]["url"]
            embed = discord.Embed(title="Random Dog Image", color=0x2F3136)
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Failed to fetch dog image :(")

    @app_commands.command(
        name="cat",
        description="Get a random cat image",
    )
    async def cat(self, interaction: discord.Interaction):
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            data = response.json()
            image_url = data[0]["url"]
            embed = discord.Embed(title="Random Cat Image", color=0x2F3136)
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Failed to fetch cat image :(")
            
def setup(bot: commands.Bot):
    bot.add_cog(ImageCommands(bot))