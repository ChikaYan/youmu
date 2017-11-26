import discord
import random
from discord.ext import commands

FELIX_ID = 272879418827866113


class Felix:
    def __init__(self, bot):
        self.bot = bot
        self._emoji_soku = discord.utils.get(bot.get_guild(241271400869003265).emojis, name="soku")

    async def on_message(self, ctx):
        if ctx.author.id == FELIX_ID and ctx.content.startswith("<@"):
            if self._emoji_soku:
                await ctx.add_reaction(self._emoji_soku)
        if ctx.author.id == FELIX_ID and random.random() > 0.5:
            if self._emoji_soku:
                await ctx.add_reaction(self._emoji_soku)

    @commands.command()
    async def fuckfelix(self, ctx):
        found = False
        async for message in ctx.channel.history():
            if message.author.id == self.bot.user.id:
                for react in message.reactions:
                    if await react.users().get(id=FELIX_ID):
                        await message.clear_reactions()
                        found = True
            if found:
                break


def setup(bot):
    bot.add_cog(Felix(bot))
