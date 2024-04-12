import discord
from discord import app_commands
from discord.ext import commands
import discord.http


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Send feedback to the bot owner")
    async def feedback(self, interaction: discord.Interaction, *, message: str):
        """Send feedback to the bot owner"""
        await interaction.response.defer()
        ctx = await self.bot.get_context(interaction)
        try:
            owner = await self.bot.fetch_user(self.bot.owner_id)
            print(owner)
        except Exception as e:
            print(e)
            owner = None
        if owner is None:
            return await interaction.edit_original_response(
                content="I'm sorry, the feedback channel isn't on yet.. please check back later."
            )
        # Send the feedback to the owner with the user's name and id,  and guild
        embed = discord.Embed(
            title="Feedback",
            description=message,
            color=discord.Color.blurple(),
        )
        embed.set_author(
            name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar.url
        )
        embed.set_footer(
            text=f"User: {interaction.user.name}#{interaction.user.discriminator} | Guild: {interaction.guild.name}"
        )
        try:
            await owner.send(embed=embed)
        except discord.Forbidden:
            return await interaction.edit_original_response(
                content="I'm sorry, the feedback channel isn't on yet.. please check back later. Maybe my owner is mad at me and so I am unable to talk to them."
            )
        await interaction.edit_original_response(content="Feedback sent!")
