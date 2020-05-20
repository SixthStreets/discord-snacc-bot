import discord
from discord.ext import commands

from snacc import utils
from snacc.classes.menus import EmbedMenu


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super(HelpCommand, self).__init__()

    async def create_start_page(self):
        bot, ctx = self.context.bot, self.context

        embed = discord.Embed(title=f"{bot.user.display_name}", color=0xff8000)

        embed.set_footer(text=bot.user.display_name, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url=bot.user.avatar_url)

        return embed

    async def get_pages(self):
        bot, ctx = self.context.bot, self.context

        all_commands = {}

        for cog, instance in bot.cogs.items():
            cmds = await self.filter_commands(instance.get_commands())
            cmds = tuple(utils.chunk_list(cmds, 10))

            for i, j in enumerate(cmds):
                doc = instance.__doc__ or ""

                all_commands[f"**{cog} | Page ({i + 1}/{len(cmds)})**\n{doc}"] = j

        pages, max_pages = [],  len(all_commands)

        home_page = await self.create_start_page()

        pages.append(home_page)

        for i, (cog, cmds) in enumerate(all_commands.items()):
            embed = discord.Embed(title=f"{bot.user.display_name}", description=cog, color=0xff8000)

            embed.set_thumbnail(url=bot.user.avatar_url)

            for cmd in cmds:
                sig = cmd.signature.replace("[", "<").replace("]", ">")

                name = f"[{'|'.join([cmd.name] + cmd.aliases)}] {sig}"

                doc = getattr(cmd.callback, "__doc__", "")

                embed.add_field(name=name, value=doc, inline=False)

            embed.set_footer(text=f"{bot.user.name} | Page {i + 1}/{max_pages}", icon_url=bot.user.avatar_url)

            pages.append(embed)

        return pages

    async def send_bot_help(self, mapping):
        pages = await self.get_pages()

        menu = EmbedMenu(pages)

        await menu.send(self.context)
