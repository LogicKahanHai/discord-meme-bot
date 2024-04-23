import discord
from discord.ext import commands
from discord import app_commands

class Whois(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="whois",
        description="Get information about a user",
    )
    async def whois(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(title="User Information", color=0x2F3136)
        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            pass
        discord_flags = user.public_flags
        discord_values = [str(flag).replace("UserFlags.", "").replace("_", " ").title() for flag in discord_flags.all()]
        if discord_values:
            discord_text = "\n".join(discord_values)
            embed.add_field(name=f"Discord Flags", value=f"{discord_text}", inline=True)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(user.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Joined Discord", value=f"<t:{int(user.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Avatar URL", value=user.avatar.url, inline=True)
        if user == user.guild.owner:
                embed.add_field(name="Role", value="Server Owner", inline=True)
        elif user.guild_permissions.administrator:
                embed.add_field(name="Role", value="Administrator", inline=True)
        elif user.guild_permissions.manage_messages:
                embed.add_field(name="Role", value="Moderator", inline=True)
        else:
            embed.add_field(name="Role", value="Member", inline=True)
        await interaction.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Whois(bot))