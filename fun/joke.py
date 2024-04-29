import discord
from discord.ext import commands
from discord import app_commands
import requests

class JokeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="joke",
        description="Get a random joke",
    )
    async def joke(self, interaction: discord.Interaction):
        try:
            url = 'https://official-joke-api.appspot.com/random_joke'
            response = requests.get(url)
            data = response.json()
            joke_setup = data['setup']
            joke_punchline = data['punchline']
            await interaction.response.send_message(f"**Joke:** {joke_setup}\n**Punchline:** {joke_punchline}")
        except Exception as e:
            await interaction.response.send_message("Failed to fetch joke :(")

def setup(bot: commands.Bot):
    bot.add_cog(JokeCommand(bot))