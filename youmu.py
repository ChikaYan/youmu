import discord
from discord.ext import commands
import asyncio

youmu = discord.ext.commands.Bot(command_prefix="!?",
                                 description="Discord bot to deal with touhou stuff",
                                 pm_help=True)
japDic = {
    "ぁ": "a", "あ": "a", "ぃ": "i", "い": "i", "ぅ": "u", "う": "u", "ぇ": "e", "え": "e", "ぉ": "o", "お": "o", "か": "ka",
    "が": "ga", "き": "ki", "ぎ": "gi", "く": "ku"
    # ぐ	け	げ	こ	ご	さ	ざ	し	じ	す	ず	せ	ぜ	そ	ぞ	た
    # だ	ち	ぢ	っ	つ	づ	て	で	と	ど	な	に	ぬ	ね	の	は
    # ば	ぱ	ひ	び	ぴ	ふ	ぶ	ぷ	へ	べ	ぺ	ほ	ぼ	ぽ	ま	み
    # む	め	も	ゃ	や	ゅ	ゆ	ょ	よ	ら	り	る	れ	ろ	ゎ	わ
    # ゐ	ゑ	を	ん	ゔ	ゕ	ゖ
}


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


keyConfig = open("key.config", "r")
youmu.run(keyConfig.readline())
