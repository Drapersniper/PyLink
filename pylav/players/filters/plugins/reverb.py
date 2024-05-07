from __future__ import annotations

from pylav.players.filters.misc import FilterMixin


class Reverb(FilterMixin):
    __slots__ = ("_delays", "_gains", "_default")

    def __init__(self, delays: list[float] | None = None, gains: list[float] | None = None) -> None:
        super().__init__()
        self._delays = delays
        self._gains = gains

    def to_dict(self) -> dict[str, float | bool | None]:
        return {
            "delays": self.delays,
            "gains": self.gains,
        }

    @classmethod
    def from_dict(cls, data: dict[str, float | bool | None]) -> Reverb:
        return cls(delays=data["delays"], gains=data["gains"])

    def __repr__(self) -> str:
        return f"<Reverb: delays={self.delays}, gains={self.gains}>"

    @property
    def delays(self) -> list[float] | None:
        return self._delays

    @delays.setter
    def delays(self, v: list[float] | None) -> None:
        if v is None:
            self._delays = None
            return
        if any(x <= 0 for x in v):
            raise ValueError(f"Delays must be must be greater than 0, not {v}")
        self._delays = v

    @property
    def gains(self) -> list[float] | None:
        return self._gains

    @gains.setter
    def gains(self, v: list[float] | None) -> None:
        if v is None:
            self._gains = v
            return
        if any(x <= 0 for x in v):
            raise ValueError(f"Gains must be must be greater than 0, not {v}")
        self._gains = v

    @classmethod
    def default(cls) -> Reverb:
        return cls()

    def get(self) -> dict[str, list[float]]:
        if self.off:
            return {}
        response = {}
        if self.delays is not None:
            response["delays"] = self.delays
        if self.gains is not None:
            response["gains"] = self.gains
        return response

    def reset(self) -> None:
        self.delays = self.gains = None
