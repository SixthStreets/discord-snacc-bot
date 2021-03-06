import discord

from discord.ext import commands


async def send_system_channel(guild, message):
    channels = [guild.system_channel] + guild.text_channels

    for c in channels:
        try:
            await c.send(message)

        except (AttributeError, discord.Forbidden, discord.HTTPException):
            continue

        break


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        """ Called when the bot joins a new server. """

        msg = f"The infamous **{self.bot.user.name}** has graced your ~~lowly~~ server! [{guild.owner.mention}]"

        await send_system_channel(guild, msg)

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        """ Called when a member joins a server. """

        svr = await self.bot.get_server(member.guild)

        if not svr.get("display_joins"):
            return

        msg = f"Welcome {member.mention} to {member.guild.name}!"

        try:
            role = member.guild.get_role(svr["default_role"])

            if role is not None:
                await member.add_roles(role)

        except (discord.Forbidden, discord.HTTPException):
            """ We failed to add the role. """

        await send_system_channel(member.guild, msg)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        """ Called when a member leaves a server. """

        svr = await self.bot.get_server(member.guild)

        if svr.get("display_joins"):
            msg = f"**{str(member)}** " + (f"({member.nick}) " if member.nick else "") + "has left the server"

            await send_system_channel(member.guild, msg)


def setup(bot):
    import os

    if not os.getenv("DEBUG", False):
        bot.add_cog(Listeners(bot))
