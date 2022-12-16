from sqlalchemy import Column, BigInteger, String, ARRAY, Float

from database.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    crypto_pairs = Column(ARRAY(String(15)))
    percent = Column(Float, default=5)
