from __future__ import annotations

import dataclasses
from typing import Annotated

from pylav.nodes.api.responses.filters.misc import ValueRangeList


@dataclasses.dataclass(repr=True, frozen=True, kw_only=True, slots=True)
class Reverb:
    delays: Annotated[list[float] | None, ValueRangeList(min=0, max=float("inf"))] = None
    gains: Annotated[list[float] | None, ValueRangeList(min=0, max=float("inf"))] = None

    def to_dict(self) -> dict[str, list[float]]:
        response: dict[str, list[float]] = {}
        if self.delays is not None:
            response["delays"] = self.delays
        if self.gains is not None:
            response["gains"] = self.gains
        return response
