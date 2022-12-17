from sqlalchemy import Column, BigInteger, JSON, Float

from database.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    crypto_pairs = Column(JSON, default={})
    percent = Column(Float, default=5)
