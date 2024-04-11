from discord import Embed
from discord.ext import commands
import requests
import random


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("meme", brief="This is a meme!")
    async def meme(self, ctx):
        memeSubreddits = [
            "dankmemes",
            "memes",
            "wholesomememes",
            "ProgrammerHumor",
            "techhumor",
            "devhumor",
            "funny",
        ]
        randomSubreddit = random.choice(memeSubreddits)
        response = requests.get(f"https://meme-api.com/gimme/{randomSubreddit}")
        if response.status_code == 200:
            data = response.json()
            meme = data["url"]
            title = data["title"]
            nsfw = data["nsfw"]
            subreddit = data["subreddit"]
            postLink = data["postLink"]
            author = data["author"]
            # embed = Embed(title=title, color=0xFF0000)
            # embed.set_image(url=meme)
            # embed.add_field(name="Author", value=author, inline=False)
            # embed.add_field(name="Subreddit", value=subreddit, inline=False)
            # embed.add_field(name="NSFW", value=nsfw, inline=False)
            # embed.add_field(name="Post Link", value=postLink, inline=False)
            color = random.randint(0, 0xFFFFFF)
            embed = Embed(
                title=title,
                description="",
                color=color,
            )
            embed.set_image(url=meme)
            embed.set_footer(text=f"Posted by u/{author} on r/{subreddit}")
            embed.add_field(
                name="", value="**[Post Link](" + postLink + ")**", inline=False
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch meme")


def setup(client):
    client.add_cog(Meme(client))
