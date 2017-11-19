#!/usr/bin/env python

import discord
from discord.ext import commands
import asyncio
from config.keyconfig import key

youmu = discord.ext.commands.Bot(command_prefix="!?",
                                 description="Discord bot to deal with touhou stuff",
                                 pm_help=True)

@youmu.event
async def on_ready():
    print('Logged in as')
    print(youmu.user.name)
    print(youmu.user.id)
    print('------')


@youmu.command()
async def test(message):
    tmp = await message.channel.send('Calculating messages...')
    counter = 0
    async for log in message.channel.history():
        if await if_jap(log):
            counter += 1

    await tmp.edit()


async def if_jap(message):
    for char in message.content:
        if char in japDic:
            return True
    return False


youmu.run(key)
