from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from crypto_checker.core.models import dto
from .base import Base


class CryptoPair(Base):
    __tablename__ = "crypto_pairs"
    __mapper_args__ = {"eager_defaults": True}

    name: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(16, 8), nullable=False)

    def to_dto(self) -> dto.CryptoPair:
        return dto.CryptoPair(name=self.name, user_id=self.user_id, price=self.price)

    @classmethod
    def from_dto(cls, pair_dto: dto.CryptoPair) -> "CryptoPair":
        return cls(
            name=pair_dto.name,
            user_id=pair_dto.user_id,
            price=pair_dto.price,
        )
