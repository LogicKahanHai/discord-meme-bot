import discord
from discord.ext import commands
from discord import app_commands

class MemberCount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="membercount",
        description="Get the member count of the server",
    )
    async def membercount(self, interaction: discord.Interaction):
        member_count = interaction.guild.member_count
        embed = discord.Embed(
            title="Member Count",
            description=f"Total Members: {member_count}",
            color=0x2F3136,
        )
        await interaction.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(MemberCount(bot))