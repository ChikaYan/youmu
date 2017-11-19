#!/usr/bin/env python

import discord
from discord.ext import commands
import asyncio
from config.keyconfig import KEY
from config.japdicconfig import JAPDIC
from config.sokuhostconfig import hosts

hostlist = {}

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
        if char in JAPDIC:
            return True
    return False


@youmu.command()
async def addhost(ctx, ip):
    if await valid_ip(ip):
        hosts[ctx.author.id] = ip
        f = open("./config/sokuhostconfig.py", "w")
        f.write("hosts = " + repr(hosts))
        f.close()
        await ctx.channel.send("Host IP has been added")
    else:
        await ctx.channel.send("Invalid IP format")
        await ctx.channel.send("Example: {}".format(hosts["example"]))


async def valid_ip(ip):
    if ip.count(":") != 1 or ip.count(".") != 3:
        return False
    return True


@youmu.command()
async def host(ctx):
    global hostlist
    if ctx.author.id in hosts:
        hostlist[ctx.author] = await ctx.channel.send("{} hosting at {}".format(ctx.author.name, hosts[ctx.author.id]))
    else:
        await ctx.channel.send("Unknown host!")
        await ctx.channel.send("Please record your IP using !?addhost first")


@youmu.command()
async def endhost(ctx):
    global hostlist
    if ctx.author in hostlist:
        await hostlist[ctx.author].edit(content="{} has ended hosting".format(ctx.author.name))
        hostlist.pop(ctx.author)


youmu.run(KEY)
