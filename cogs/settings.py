import logging
import discord

from discord import SlashCommandGroup, ApplicationContext
from discord.ext import commands
from discord.commands import Option
from .util.config import Config

log = logging.getLogger(__name__)


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    config = SlashCommandGroup(
        "config",
        "Setup server and change settings for temporary channels.",
        checks=[commands.has_permissions(administrator=True).predicate],
    )

    @config.command(name="setup")
    async def setup_guild(
        self,
        ctx: ApplicationContext,
    ):
        try:
            await self.config.setup_guild(ctx)
        except Exception as e:
            log.exception(f"setup_guild,{type(e)} error occured,{e}")
            await ctx.respond("Failed to setup the Server.")

    @config.command(name="view")
    async def view_config(
        self,
        ctx: ApplicationContext,
    ):
        try:
            conf = self.config.get_all(ctx.guild.id)
            await ctx.respond(f"{conf}")
        except Exception as e:
            log.exception(f"setup_guild,{type(e)} error occured,{e}")
            await ctx.respond("Failed to get the Config. Try `/config setup`.")

    @config.command(name="set_role")
    async def set_member_role(
        self,
        ctx: ApplicationContext,
        role: Option(discord.Role, "role monitored for Live Streamers"),
    ):
        """Set the role the bot will monitor for Live Streamers"""
        try:
            self.config.set(ctx.guild.id, "member_role_id", role.id)
            await ctx.respond(f"Changed role to @**{role.name}**")
        except Exception as e:
            log.exception(f"set_member_role,{type(e)} error occured,{e}")
            await ctx.respond("Failed to set the role.")


def setup(bot):
    bot.add_cog(Settings(bot))
