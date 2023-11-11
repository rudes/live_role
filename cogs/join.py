import logging

from discord.ext import commands
from .util.config import Config

log = logging.getLogger(__name__)


class JoinGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await self.config.setup_request(guild)
        except Exception as e:
            log.exception(f"on_guild_join,{type(e)} error occured,{e}")


def setup(bot):
    bot.add_cog(JoinGuild(bot))
