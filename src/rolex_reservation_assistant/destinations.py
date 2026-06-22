from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class Destination:
    key: str
    label: str
    url: str

    @property
    def hostname(self) -> str:
        return urlparse(self.url).hostname or ""


DESTINATIONS: dict[str, Destination] = {
    "osaka-umeda": Destination(
        key="osaka-umeda",
        label="大阪",
        url="https://reservation.rolexboutique-hiltonplaza-osaka.jp/osaka-umeda/reservation",
    ),
    "ginza": Destination(
        key="ginza",
        label="銀座",
        url="https://reservation.rolexboutique-lexia.jp/ginza/reservation",
    ),
    "omotesando": Destination(
        key="omotesando",
        label="表参道",
        url=(
            "https://reservation.rolexboutique-omotesando-tokyo.jp/omotesando/reservation"
            "?func_distinction=1"
        ),
    ),
    "shinjuku": Destination(
        key="shinjuku",
        label="新宿",
        url="https://reservation.rolexboutique-lexia.jp/shinjuku/reservation",
    ),
    "nagoya-sakae": Destination(
        key="nagoya-sakae",
        label="名古屋栄",
        url="https://reservation.rolexboutique-lexia.jp/nagoya-sakae/reservation",
    ),
}


def list_destination_keys() -> list[str]:
    return [*DESTINATIONS.keys()]


def resolve_destinations(location: str) -> list[Destination]:
    if location == "all":
        return [DESTINATIONS[key] for key in list_destination_keys()]
    try:
        return [DESTINATIONS[location]]
    except KeyError as exc:
        valid = ", ".join(["all", *list_destination_keys()])
        raise ValueError(f"Unknown location: {location}. Valid locations: {valid}") from exc
