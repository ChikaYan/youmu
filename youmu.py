#!/usr/bin/env python

import discord
from discord.ext import commands
import asyncio
from config.keyconfig import KEY
from config.japdicconfig import JAPDIC
from config.sokuhostconfig import hosts
from config.hamachiconfig import rooms

hostlist = {}

youmu = discord.ext.commands.Bot(command_prefix="!?",
                                 description="Discord bot to deal with touhou stuff",
                                 pm_help=True)


@youmu.event
async def on_ready():
    print("Logged in as")
    print(youmu.user.name)
    print(youmu.user.id)
    print("------")


# @youmu.event
# async def on_message(ctx):
#     if ctx.content.startswith("谢指教"):
#         await ctx.channel.send("<@{}>谢你个头".format(ctx.author.id))


@youmu.command()
async def addhost(ctx, *args):
    if args:
        ip = args[0]
        hamachi = False
        room = ""
        if len(args) == 3:
            if args[1] == "hamachi":
                hamachi = True
                room = args[2]
        if await valid_ip(ip):
            hosts[ctx.author.id] = {"IP": ip, "hamachi": hamachi, "roomID": room}
            f = open("./config/sokuhostconfig.py", "w")
            f.write("hosts = " + repr(hosts))
            f.close()
            await ctx.channel.send("Host IP has been added.")
            if not hamachi:
                await ctx.channel.send("Add `hamachi [hamachi room name]` to indicate you are using hamachi.")
        else:
            await ctx.channel.send("Invalid IP format")
            await ctx.channel.send("Example: {}".format(hosts["example"]["IP"]))


async def valid_ip(ip):
    if ip.count(":") != 1 or ip.count(".") != 3:
        return False
    return True


@youmu.command()
async def host(ctx):
    global hostlist
    if ctx.author.id in hosts:
        text = "`{}` hosting at `{}`".format(ctx.author.name, hosts[ctx.author.id]["IP"])
        if hosts[ctx.author.id]["hamachi"]:
            text += "\n with hamachi ID: `{}` PW: `{}`".format(hosts[ctx.author.id]["roomID"],
                                                               rooms[hosts[ctx.author.id]["roomID"]])
        hostlist[ctx.author] = await ctx.channel.send(text)
    else:
        await ctx.channel.send("Unknown host!")
        await ctx.channel.send("Please record your IP using !?addhost first.")


@youmu.command()
async def endhost(ctx):
    global hostlist
    if ctx.author in hostlist:
        await hostlist[ctx.author].edit(content="{} has ended hosting.".format(ctx.author.name))
        hostlist.pop(ctx.author)


@youmu.command()
async def addhamachi(ctx, roomid, pw):
    rooms[roomid] = pw
    await ctx.channel.send("Hamachi room information has been added.")
    f = open("./config/hamachiconfig.py", "w")
    f.write("rooms = " + repr(rooms))
    f.close()


youmu.run(KEY)
