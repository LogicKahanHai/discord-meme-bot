import discord
from discord.ext import commands
from discord import app_commands
import requests

class UserAvatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="avatar",
        description="Get the avatar of your own avatar",
    )
    async def myphoto(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=f"{interaction.user.name} Aavatar", color=0x2F3136)
            embed.set_image(url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Failed to fetch user avatar :(")
            print(e)
    
def setup(bot: commands.Bot):
    bot.add_cog(UserAvatar(bot))