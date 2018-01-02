from pixivpy3 import *
from config.pixivconfig import userid, pw, idnum
import discord
import asyncio
from discord.ext import commands
from time import gmtime, strftime
import os


class Pixiv:
    def __init__(self, bot):
        self.bot = bot
        self.api = AppPixivAPI()
        self.search_depth = 50000
        self.bot.loop.create_task(self.daily_touhou())

    async def daily_touhou(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(383359073229209611)
        while not self.bot.is_closed():
            if strftime("%H:%M", gmtime()) == "07:30":
                await self.send_pic(channel, "東方", 1000)
                await asyncio.sleep(86400)
            else:
                await asyncio.sleep(59)

    @commands.command()
    async def gimme2hu(self, ctx):
        await self.send_pic(ctx.channel, "東方", 100)

    async def send_pic(self, channel, tag, mark_min):
        self.api.login(userid, pw)  # login every time before getting json result
        json_result = self.api.search_illust(tag, req_auth=True)
        for i in range(self.search_depth):
            for illust in json_result.illusts:
                if illust.total_bookmarks >= mark_min and not illust.is_bookmarked:
                    # the pic is popular and has not been sent before
                    self.api.download(illust.image_urls.large, name="temp.jpg", path="./img", )
                    await channel.send(file=discord.File("./img/temp.jpg"))
                    self.api.illust_bookmark_add(illust.id)
                    os.remove("./img/temp.jpg")
                    return
            next_page = self.api.parse_qs(json_result.next_url)
            json_result = self.api.search_illust(**next_page)

        # search depth reached -- need to clean bookmarks

    async def clean_bookmarks(self):
        json_result = self.api.user_illusts(idnum, req_auth=True)
        for illust in json_result.illusts:
            self.api.illust_bookmark_delete(illust.id)


def setup(bot):
    bot.add_cog(Pixiv(bot))
