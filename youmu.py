#!/usr/bin/env python

import discord
import random
from discord.ext import commands
import asyncio
from config.keyconfig import KEY
from config.sokuhostconfig import hosts
from config.hamachiconfig import rooms

hostlist = {}
youmu = discord.ext.commands.Bot(command_prefix="!?",
                                 description="Discord bot to deal with touhou stuff",
                                 pm_help=True)
emoji_soku = None


@youmu.event
async def on_ready():
    global emoji_soku
    print("Logged in as")
    print(youmu.user.name)
    print(youmu.user.id)
    print("------")
    emoji_soku = discord.utils.get(youmu.get_guild(241271400869003265).emojis, name="soku")


@youmu.event
async def on_message(ctx):
    if ctx.content.startswith("谢指教"):
        await ctx.channel.send("<@{}>谢你个头".format(ctx.author.id))
    if ctx.author.id == 272879418827866113 and ctx.content.startswith("<@"):
        if emoji_soku:
            await ctx.add_reaction(emoji_soku)
    if ctx.author.id == 272879418827866113 and random.random() > 0.5:
        if emoji_soku:
            await ctx.add_reaction(emoji_soku)
    await youmu.process_commands(ctx)


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
            await ctx.message.add_reaction(emoji_soku)
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
async def host(ctx, *args):
    global hostlist
    txt = ""
    if args:
        for arg in args:
            txt += arg + " "
        txt = ":speaking_head: `{}`".format(txt)

    if ctx.author.id in hosts:
        text = "`{}` hosting at `{}` {}".format(ctx.author.name, hosts[ctx.author.id]["IP"], txt)
        if hosts[ctx.author.id]["hamachi"]:
            text += "\n with hamachi ID: `{}` PW: `{}`".format(hosts[ctx.author.id]["roomID"],
                                                               rooms[hosts[ctx.author.id]["roomID"]])
        hostlist[ctx.author] = await ctx.channel.send(text)
        await ctx.message.add_reaction(emoji_soku)
    else:
        await ctx.channel.send("Unknown host!")
        await ctx.channel.send("Please record your IP using !?addhost first.")


@youmu.command()
async def endhost(ctx):
    global hostlist
    if ctx.author in hostlist:
        await hostlist[ctx.author].edit(content="{} has ended hosting.".format(ctx.author.name))
        hostlist.pop(ctx.author)
    await ctx.message.add_reaction(emoji_soku)


@youmu.command()
async def addhamachi(ctx, roomid, pw):
    rooms[roomid] = pw
    await ctx.channel.send("Hamachi room information has been added.")
    f = open("./config/hamachiconfig.py", "w")
    f.write("rooms = " + repr(rooms))
    f.close()


@youmu.command()
async def showhost(ctx):
    for current_host in hostlist.keys():
        text = "`{}` hosting at `{}`".format(current_host.name, hosts[current_host.id]["IP"])
        if hosts[current_host.id]["hamachi"]:
            text += "\n with hamachi ID: `{}` PW: `{}`".format(hosts[current_host.id]["roomID"],
                                                               rooms[hosts[current_host.id]["roomID"]])
        await ctx.channel.send(text)
    await ctx.message.add_reaction(emoji_soku)


@youmu.command()
async def givemesoku(ctx):
    await ctx.channel.send("Here you are:\nhttps://mega.nz/#!ccJhWTYA!pOezX4yFenh5o1_k55KCSF34fXv8EdkvLHu97m-kXZ4")
    await ctx.message.add_reaction(emoji_soku)


@youmu.command()
async def glossary(ctx):
    await ctx.channel.send("https://hisouten.koumakan.jp/wiki/Glossary")
    await ctx.message.add_reaction(emoji_soku)


@youmu.command()
async def fuckfelix(ctx):
    found = False
    async for message in ctx.channel.history():
        if message.author.id == youmu.user.id:
            for react in message.reactions:
                if await react.users().get(id=272879418827866113):
                    await message.clear_reactions()
                    found = True
        if found:
            break

youmu.run(KEY)
