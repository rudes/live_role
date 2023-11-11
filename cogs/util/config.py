"""class for managing the Config"""
import logging
import json
import redis
import discord

log = logging.getLogger(__name__)


class RoleSelect(discord.ui.View):
    @discord.ui.role_select(placeholder="Twitch Subscriber")
    async def role_select_dropdown(
        self, select: discord.ui.Select, ctx: discord.Interaction
    ):
        try:
            member_role = select.values[0]
            live_role = await ctx.guild.create_role(
                name="Live", hoist=True, color=11174623
            )
            conf = {
                "live_role_id": live_role.id,
                "member_role_id": member_role.id,
            }
            db = redis.StrictRedis(host="db")
            db.set(str(ctx.guild.id), json.dumps(conf))
            await ctx.response.send_message(
                "Discord setup, you'll need to move the `Live` role higher up in your discord settings, unfortunately I'm not able to."
            )
        except Exception as e:
            log.exception(f"role_select_dropdown,{type(e)} error occured,{e}")
            await ctx.response.send_message("Failed to setup the Discord")


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
        view = RoleSelect()
        await ctx.respond("Choose the role we'll monitor for streamers", view=view)

    async def setup_request(self, guild):
        """let people know to setup the bot"""
        chan = None
        for c in guild.text_channels:
            if c.permissions_for(guild.me).send_messages:
                chan = c
        if not chan:
            return
        message = "Thank you for adding **Live Streaming Role**.\nTo setup have someone with admin rights use `/config setup`."
        async for m in chan.history(limit=100):
            if message == m.content:
                return
        await chan.send(message)
