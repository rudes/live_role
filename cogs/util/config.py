"""class for managing the Config"""
import logging
import json
import redis
import discord

log = logging.getLogger(__name__)


class ConfigModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.Select(
                select_type=discord.ComponentType.role_select,
                placeholder="Twitch Subscriber",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, ctx: discord.Interaction):
        member_role = self.children[0].value
        live_role = await ctx.guild.creat_role("Live", hoist=True, color=11174623)
        await ctx.guild.edit_role_positions(postions={live_role: 2})
        conf = {
            "live_role_id": live_role.id,
            "member_role_id": member_role.id,
        }
        db = redis.StrictRedis(host="db")
        db.set(str(ctx.guild.id), json.dumps(conf))
        await ctx.response.send_message("Config created.")


class Config:
    """class for managing the Config"""

    def __init__(self):
        self.db = redis.StrictRedis(host="db")

    def get(self, guild_id, setting):
        """get a specific value from the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        return config_json[setting]

    def get_all(self, guild_id):
        """get the full config from the db"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        return config_json

    def set(self, guild_id, setting, value):
        """set a specific value to the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        config_json[setting] = value
        config_string = json.dumps(config_json)
        self.db.set(str(guild_id), config_string)

    async def setup_guild(self, ctx):
        """prepare the discord for tinyrooms"""
        modal = ConfigModal(title="Choose the role the bot will monitor for streamers.")
        await ctx.send_modal(modal)

    async def setup_request(self, guild):
        """let people know to setup the bot"""
        chan = None
        for c in guild.text_channels:
            if c.permissions_for(guild.me).send_messages:
                chan = c
        if not chan:
            return
        message = "Thank you for adding {self.bot.mention}\nTo setup have someone with admin rights use `/config setup`."
        async for m in chan.history(limit=100):
            if message == m.content:
                return
        await chan.send(message)
