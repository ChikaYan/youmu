#!/usr/bin/env python

from discord.ext import commands
from config.keyconfig import KEY
import logging

bot = commands.Bot(command_prefix="!?",
                   description="Discord bot to deal with touhou stuff",
                   pm_help=True)
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    bot.load_extension("cogs.soku")
    bot.load_extension("cogs.felix")
    bot.load_extension("cogs.romaji")
    bot.load_extension("cogs.pixiv")

bot.run(KEY)
