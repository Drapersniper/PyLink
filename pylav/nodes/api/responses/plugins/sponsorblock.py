from __future__ import annotations

import dataclasses
from typing import Literal

from pylav.nodes.api.responses.websocket import Message

__all__ = ("Segment", "SegmentsLoaded", "SegmentSkipped")

from pylav.type_hints.dict_typing import JSON_DICT_TYPE


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class Segment:
    category: str
    start: str
    end: str


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class SegmentsLoaded(Message):
    op: Literal["event"] = "event"
    guildId: str | None = None
    type: Literal["SegmentsLoadedEvent"] = "SegmentsLoadedEvent"
    segments: list[Segment | JSON_DICT_TYPE] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        temp = []
        for s in self.segments:
            if isinstance(s, Segment) or (isinstance(s, dict) and (s := Segment(**s))):
                temp.append(s)
        object.__setattr__(self, "segments", temp)


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class SegmentSkipped(Message):
    op: Literal["event"] = "event"
    guildId: str | None = None
    type: Literal["SegmentSkippedEvent"] = "SegmentSkippedEvent"
    segment: Segment | JSON_DICT_TYPE = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.segment, dict):
            object.__setattr__(self, "segment", Segment(**self.segment))
