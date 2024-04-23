import discord
from discord import app_commands
from discord.ext import commands
import discord.http
from discord.ext.commands import Bot
from utils.db import DB


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.cursor = DB()

    @app_commands.command(name="feedback", description="Send feedback to the bot owner")
    async def feedback(self, interaction: discord.Interaction, *, message: str):
        """Send feedback to the bot owner"""
        await interaction.response.defer()
        ctx = await self.bot.get_context(interaction)
        try:
            owner = await self.bot.fetch_user(self.bot.owner_id)
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

    @app_commands.command(
        name="help",
        description="Get the list of all commands that I can perform!",
    )
    async def help(self, interaction: discord.Interaction):
        embedVar = discord.Embed(
            title="AWS ka Chotu aa gaya!",
            description="I send memes and important tech news on the topics that the masters of this server have selected. You can find the list of all my commands below: -",
            color=0x00FF00,
        )
        allCogs = self.bot.cogs
        for cog in allCogs:
            commands = self.bot.get_cog(cog).get_app_commands()
            cog_commands = ""
            for command in commands:
                cog_commands += f"**{command.name}** - {command.description}\n"
            embedVar.add_field(
                name=f"**__{cog}__**\n\n", value=cog_commands, inline=False
            )
        await interaction.response.send_message(embed=embedVar)

    @app_commands.command(
        name="suggest-feature",
        description="Suggest a feature for the bot",
    )
    async def suggest_feature(self, interaction: discord.Interaction, *, feature: str):
        await interaction.response.defer()

        # feature = (
        #     f"{interaction.user.name}{f"#{interaction.user.discriminator}" if interaction.user.discriminator != "0" else ""} - {feature}"
        # )
        suggestion = {
            "user": f"{interaction.user.name}{f"#{interaction.user.discriminator}" if interaction.user.discriminator != "0" else ""}",
            "suggestion": feature,
            "votes": 1,
        }
        self.cursor.add("suggested_features", suggestion)
        embed = discord.Embed(
            title="Success!",
            description="Feature has been suggested successfully!",
            color=discord.Color.green(),
        )
        await interaction.edit_original_response(embed=embed)
