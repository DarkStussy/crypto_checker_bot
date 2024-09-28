from dataclasses import dataclass, field
from decimal import Decimal

from .pair import CryptoPair


@dataclass(slots=True)
class User:
    id: int
    percent: Decimal
    pairs: list[CryptoPair] = field(default_factory=list)

    def remove_pair(self, pair_name: str):
        self.pairs = [pair for pair in self.pairs if pair.name != pair_name]
