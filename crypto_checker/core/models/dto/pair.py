from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class CryptoPair:
    name: str
    user_id: int
    price: Decimal
