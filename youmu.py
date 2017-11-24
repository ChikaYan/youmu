#!/usr/bin/env python

import discord
import random
from discord.ext import commands
import asyncio
from config.keyconfig import KEY

bot = discord.ext.commands.Bot(command_prefix="!?",
                               description="Discord bot to deal with touhou stuff",
                               pm_help=True)

emoji_soku = None


@bot.event
async def on_ready():
    global emoji_soku
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    emoji_soku = discord.utils.get(bot.get_guild(241271400869003265).emojis, name="soku")
    bot.load_extension("cogs.soku")


@bot.event
async def on_message(ctx):
    if ctx.content.startswith("谢指教"):
        await ctx.channel.send("<@{}>谢你个头".format(ctx.author.id))
    if ctx.author.id == 272879418827866113 and ctx.content.startswith("<@"):
        if emoji_soku:
            await ctx.add_reaction(emoji_soku)
    if ctx.author.id == 272879418827866113 and random.random() > 0.5:
        if emoji_soku:
            await ctx.add_reaction(emoji_soku)
    await bot.process_commands(ctx)


@bot.command()
async def fuckfelix(ctx):
    found = False
    async for message in ctx.channel.history():
        if message.author.id == bot.user.id:
            for react in message.reactions:
                if await react.users().get(id=272879418827866113):
                    await message.clear_reactions()
                    found = True
        if found:
            break


bot.run(KEY)
