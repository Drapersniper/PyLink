from __future__ import annotations

import dataclasses

from pylav.nodes.api.responses.shared import LyricsPluginInfo

__all__ = ("LyricsLine", "LyricsObject")


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class LyricsLine:
    timestamp: int
    duration: int | None
    line: str
    plugin: LyricsPluginInfo

    def __post_init__(self):
        if isinstance(self.plugin, dict) and (p := LyricsPluginInfo(**self.plugin)):
            object.__setattr__(self, "plugin", p)


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class LyricsObject:
    sourceName: str
    provider: str
    text: str | None = None
    lines: list[LyricsLine]
    plugin: LyricsPluginInfo

    def __post_init__(self):
        if isinstance(self.plugin, dict) and (p := LyricsPluginInfo(**self.plugin)):
            object.__setattr__(self, "plugin", p)
