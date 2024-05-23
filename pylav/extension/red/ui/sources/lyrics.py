from pathlib import Path

import discord
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import humanize_number
from redbot.vendored.discord.ext import menus

from pylav.extension.red.ui.menus.generic import BaseMenu
from pylav.logging import getLogger
from pylav.players.tracks.obj import Track
from pylav.type_hints.bot import DISCORD_COG_TYPE

_ = Translator("PyLav", Path(__file__))

LOGGER = getLogger("PyLav.ext.red.ui.sources.lyrics")


class LyricsSource(menus.ListPageSource):
    def __init__(self, cog: DISCORD_COG_TYPE, track: Track, pages: list[str]):
        super().__init__(pages, per_page=1)
        self.track = track
        self.cog = cog

    def get_starting_index_and_page_number(self, menu: BaseMenu) -> tuple[int, int]:
        page_num = menu.current_page
        start = page_num * self.per_page
        return start, page_num

    async def format_page(self, menu: BaseMenu, page: str) -> discord.Embed:
        __, page_num = self.get_starting_index_and_page_number(menu)
        total_number_of_entries = len(self.entries)
        current_page = humanize_number(page_num + 1)
        total_number_of_pages = humanize_number(self.get_max_pages())
        title = f"{await self.track.title()}"
        page = await self.cog.pylav.construct_embed(
            messageable=menu.ctx,
            title=title,
            description=page,
            thumbnail=await self.track.artworkUrl(),
            url=await self.track.uri(),
        )
        match total_number_of_entries:
            case 1:
                message = _("Page 1 / 1 | 1 Page")
            case 0:
                message = _("Page 1 / 1 | 0 Pages")
            case __:
                message = _(
                    "Page {current_page_variable_do_not_translate} / {total_number_of_pages_variable_do_not_translate} "
                    "| {total_number_of_entries_variable_do_not_translate} Pages"
                ).format(
                    current_page_variable_do_not_translate=current_page,
                    total_number_of_pages_variable_do_not_translate=total_number_of_pages,
                    total_number_of_entries_variable_do_not_translate=humanize_number(total_number_of_entries),
                )
        page.set_footer(text=message)

        return page
