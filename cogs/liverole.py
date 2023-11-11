import discord
import logging

from discord.ext import commands
from .util.config import Config

log = logging.getLogger(__name__)


class LiveRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_presence_update(self, _, user):
        try:
            try:
                conf = self.config.get_all(user.guild.id)
            except Exception:
                return

            live_role = user.guild.get_role(int(conf["live_role_id"]))
            for m in live_role.members:
                await self.check_status(live_role, m)

            member_role = user.guild.get_role(int(conf["member_role_id"]))
            if member_role in user.roles:
                await self.check_status(live_role, user)
        except Exception as e:
            log.exception(f"liverole,{type(e)} error occured,{e}")

    async def check_status(self, live_role, user):
        stream = None
        for activity in user.activities:
            if activity.type == discord.ActivityType.streaming:
                stream = activity

        if stream:
            if live_role in user.roles:
                return
            await user.add_roles(
                live_role,
            )
        else:
            if live_role not in user.roles:
                return
            await user.remove_roles(
                live_role,
            )


def setup(bot):
    bot.add_cog(LiveRole(bot))
