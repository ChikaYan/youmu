from pixivpy3 import *
from config.pixivconfig import userid, pw
import discord
from discord.ext import commands


class Pixiv:
    def __init__(self, bot):
        self.bot = bot
        self._api = AppPixivAPI()
        self._api.login(userid, pw)

    @commands.command()
    async def givemetouhou(self, ctx):
        json_result = self._api.search_illust("東方", req_auth=True)
        for illust in json_result.illusts:
            if illust.total_bookmarks >= 0 and not illust.is_bookmarked:
                # the pic is popular and has not been sent before
                # await self.send_pic(illust.image_urls['large'], ctx.channel)
                self._api.download(illust.image_urls.large, name="touhou.jpg", path="./pic",)
                await ctx.channel.send(file=discord.File("./pic/touhou.jpg"))
                self._api.illust_bookmark_add(illust.id)
                print(illust.image_urls['large'])
                return








def setup(bot):
    bot.add_cog(Pixiv(bot))
