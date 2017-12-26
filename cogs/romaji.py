import discord
from discord.ext import commands
from cogs.japdic import JAPDIC


class Romaji:
    def __init__(self, bot):
        self.bot = bot
        self.jap_log = []

    @commands.command()
    async def romaji(self, ctx):
        async for message in ctx.channel.history(limit=50):
            if any(key in message.content for key in
                   JAPDIC) and message.id not in self.jap_log and not message.author.bot:
                # the user-sent message contains japanese but is not converted before
                await ctx.channel.send("{}:\n{}".format(message.content, await self.convert(message.content)))
                self.jap_log.append(message.id)
                await self.clean_log()
                break

    async def convert(self, text):
        for char in text:
            if char in JAPDIC:
                text = text.replace(char, JAPDIC[char] + " ")
        return text

    async def clean_log(self):
        if len(self.jap_log) >= 100:
            self.jap_log = []


def setup(bot):
    bot.add_cog(Romaji(bot))
