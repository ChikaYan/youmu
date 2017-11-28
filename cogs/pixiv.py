from pixivpy3 import *
from config.pixivconfig import userid, pw
import discord
from discord.ext import commands
import os


class Pixiv:
    def __init__(self, bot):
        self.bot = bot
        self._api = AppPixivAPI()
        self._api.login(userid, pw)
        self._search_depth = 50000
        self._mark_min = 100

    @commands.command()
    async def gimme2hu(self, ctx):
        json_result = self._api.search_illust("東方", req_auth=True)
        for i in range(self._search_depth):
            for illust in json_result.illusts:
                if illust.total_bookmarks >= self._mark_min and not illust.is_bookmarked:
                    # the pic is popular and has not been sent before
                    self._api.download(illust.image_urls.large, name="touhou.jpg", path="./pic", )
                    await ctx.channel.send(file=discord.File("./pic/touhou.jpg"))
                    self._api.illust_bookmark_add(illust.id)
                    os.remove("./pic/touhou.jpg")
                    return
            next_page = self._api.parse_qs(json_result.next_url)
            json_result = self._api.search_illust(**next_page)


def setup(bot):
    bot.add_cog(Pixiv(bot))
