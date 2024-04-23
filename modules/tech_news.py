import discord
import re
from discord.ext import commands
from utils.get_emails import Email
import random
import asyncio
from discord import app_commands


class TechNews(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loading = False

    @app_commands.command(
        name="enlighten-me",
        description="Get a random report from the tech world, or specify a topic to get news on that topic!",
    )
    async def enlightenMe(self, interaction: discord.Interaction, topic: str = ""):
        self.loading = True
        await interaction.response.defer()
        try:
            email_class = Email()
            if topic != "" and not email_class.check_topic(topic=topic):
                topics = email_class.get_topics()
                await interaction.edit_original_response(
                    content=f"Pardon me! I could not find any news on __{topic}__. Here are some topics I can help you with:\n\n**__{'__**, **__'.join(topics)}__**\n\nPlease try again with one of these topics! **I am not very intelligent right now, so I can only understand the topic if you write it exactly as shown above (Can be in any case, lowercase, uppercase but the spelling should not be wrong)!**"
                )
                return
            await interaction.edit_original_response(content="Please wait while I book the tickets for my journey...")
            multiplier = 1
            load_news_task = asyncio.create_task(self.load_the_news(topic=topic))
            count = 0
            success = True
            while self.loading:
                count += 1
                if count > 1:
                    success = False
                    self.loading = False
                    break
                async with interaction.channel.typing():
                    await asyncio.sleep(0.5 * multiplier)
                    await interaction.edit_original_response(content="Boarding the flight...")
                    await asyncio.sleep(1 * multiplier)
                    await interaction.edit_original_response(content="Taking off...")
                    await asyncio.sleep(1 * multiplier)
                    await interaction.edit_original_response(content="Landed... Gathering the news...")
                    await asyncio.sleep(1 * multiplier)
                    await interaction.edit_original_response(content="On my way back...")
                    await asyncio.sleep(1 * multiplier)
                    await interaction.edit_original_response(content="Almost there...")
                    await asyncio.sleep(1 * multiplier)
                    await interaction.edit_original_response(content="I'm back!")
                    await asyncio.sleep(1 * multiplier)
                    if self.loading:
                        multiplier /= 2
                        if multiplier < 0.5:
                            multiplier = 0.5
                        await interaction.edit_original_response(content="Oh no! I forgot the most important part! Let me quickly go and come back...")
                        await asyncio.sleep(1 * multiplier)
            if success:
                embed = await load_news_task
                await interaction.edit_original_response(content="Finally! Here you go! You can click on the news links to go read the articles.", embed=embed)
            else:
                await interaction.edit_original_response(content="I'm sorry! I could not find any news for you. Please try again later!")
        except Exception as e:
            print(f"Error: {e}")
            await interaction.edit_original_response(content="I'm sorry! I could not find any news for you. Please try again later!")

    async def load_the_news(self, topic: str = ""):
        email = Email()
        news_with_topic = await email.get_news(topic=topic)
        try:
            news = news_with_topic["news"]
            topic: str = news_with_topic["topic"]
            links: dict = news_with_topic["links"]
        except KeyError:
            news = {}
            topic = "TLDR Tech"
        try:
            keys = news.keys()
        except AttributeError:
            keys = []

        embed = discord.Embed(
            title=f"Here is the latest tech news on __{topic.replace('TLDR ', '')}__!",
            description=f"This is what I could find for you!",
            color=0x00FF00,
        )

        if len(keys) == 0:
            embed.add_field(
                name="No News",
                value="I could not find any news for you. Please try again later!",
                inline=False,
            )
            return embed

        for key in keys:
            section_news = news[key]
            if len(section_news) == 0:
                continue
            index = random.randint(0, len(section_news) - 1)

            if section_news[index]["title"] == "" or section_news[index]["brief"] == "":
                continue

            match = re.search(r'\[(\d{1,2})\]', section_news[index]['title'])
            if match:
                link_key = int(match.group(1))

            title = re.sub(r'\[\d{1,2}\]\s*', '', section_news[index]['title'])

            link = links.get(link_key, None)

            temp = f"**[{title}]({link})**\n{section_news[index]['brief']}\n\n"

            section_title = f"**__{key.upper()}__**\n\n"

            if len(temp) + len(section_title) > 3800:
                break

            embed.add_field(name=section_title, value=temp, inline=False)

        print("News loaded successfully!")

        self.loading = False
        print(f"Loading set to {self.loading}")
        return embed
