import discord
from discord.ext import commands
from discord import app_commands
from utils.db import DB


class FuturePlans(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cursor = DB()

    def check_owner(self, interaction: discord.Interaction):
        return str(interaction.user.id) == self.bot.owner_id

    # Check if the command is being used in Private Message
    async def is_private(self, interaction: discord.Interaction):
        if interaction.channel.type == discord.ChannelType.private:
            embed = discord.Embed(
                title="Error!",
                description="This command can only be used in a server!",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(embed=embed)
            return True
        return False

    # Check if the command is being used in a Guild
    async def is_guild(self, interaction: discord.Interaction):
        if interaction.channel.type != discord.ChannelType.private:
            embed = discord.Embed(
                title="Error!",
                description="This command can only be used in a private message and by the OWNER only! Use the `/suggest-feature` command to suggest anything.",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(embed=embed)
            return True
        return False

    @app_commands.command(
        name="future-plans",
        description="Get the future plans for the bot",
    )
    async def future_plans(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.is_private(interaction):
            return
        future_plans = self.cursor.get("future_plans")
        if future_plans:
            plans = "\n".join(future_plans)
        embed = discord.Embed(
            title="Future Plans",
            description=plans if future_plans else "No future plans set yet!",
            color=discord.Color.blurple(),
        )
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(
        name="add-future-plan",
        description="Set the future plans for the bot",
    )
    async def add_future_plan(
        self, interaction: discord.Interaction, *, future_plan: str
    ):
        await interaction.response.defer()
        if await self.is_guild(interaction):
            return
        if not self.check_owner(interaction):
            embed = discord.Embed(
                title="Error!",
                description="You are not authorized to set future plans!",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(
                embed=embed,
            )
            return
        last_id = self.cursor.get("future_plans_last_id")
        if not last_id:
            self.cursor.set("future_plans_last_id", 0)
            last_id = 0
        future_plan = f"{str(last_id + 1).zfill(3)} - {future_plan}"
        self.cursor.add("future_plans", future_plan)
        self.cursor.set("future_plans_last_id", last_id + 1)
        future_plans = self.cursor.get("future_plans")
        embed = discord.Embed(
            title="Success!",
            description="Future plans have been set successfully!",
            color=discord.Color.green(),
        )
        plans = "\n".join(future_plans)
        embed.add_field(name="Future Plans", value=plans)
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(
        name="mark-future-plan-complete",
        description="Remove a future plan for the bot",
    )
    async def mark_future_plan_complete(
        self, interaction: discord.Interaction, *, future_plan_id: int
    ):
        await interaction.response.defer()
        if await self.is_guild(interaction):
            return
        if not self.check_owner(interaction):
            embed = discord.Embed(
                title="Error!",
                description="You are not authorized to mark future plans as complete!",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(
                embed=embed,
            )
            return

        future_plans = self.cursor.get("future_plans")
        if not future_plans:
            embed = discord.Embed(
                title="Error!",
                description="No future plans set yet!",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(embed=embed)
            return
        completed = ""
        for plan in future_plans:
            if plan.startswith(f"{str(future_plan_id).zfill(3)} - "):
                completed = plan
                future_plans.remove(plan)
                break

        if not completed:
            embed = discord.Embed(
                title="Error!",
                description="No future plan found with the given ID!",
                color=discord.Color.red(),
            )
            await interaction.edit_original_response(embed=embed)
            return

        self.cursor.add("completed_plans", completed)

        self.cursor.set("future_plans", future_plans)
        embed = discord.Embed(
            title="Success!",
            description="Future plan has been marked as complete!",
            color=discord.Color.green(),
        )
        plans = "\n".join(future_plans)
        embed.add_field(name="Future Plans", value=plans)
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(
        name="completed-plans",
        description="Get the completed plans for the bot",
    )
    async def completed_plans(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.is_private(interaction):
            return
        completed_plans = self.cursor.get("completed_plans")
        if completed_plans:
            plans = "\n".join(completed_plans)
        embed = discord.Embed(
            title="Completed Plans",
            description=plans if completed_plans else "No completed plans yet!",
            color=discord.Color.blurple(),
        )
        await interaction.edit_original_response(embed=embed)
