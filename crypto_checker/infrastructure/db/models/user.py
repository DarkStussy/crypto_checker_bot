from decimal import Decimal

from sqlalchemy import BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crypto_checker.core.models import dto
from . import CryptoPair
from .base import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    percent: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    pairs: Mapped[list[CryptoPair]] = relationship()

    def to_dto(self, with_pairs: bool = True) -> dto.User:
        return dto.User(
            id=self.id,
            percent=self.percent,
            pairs=[pair.to_dto() for pair in self.pairs] if with_pairs else [],
        )

    @classmethod
    def from_dto(cls, user_dto: dto.User) -> "User":
        return cls(id=user_dto.id, percent=user_dto.percent)
