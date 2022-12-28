import typing

from sqlalchemy import select

from database.models.user import User


class BaseGateway:
    def __init__(self, session):
        self.session = session


class Gateway(BaseGateway):
    """Database gateway"""

    async def merge(self, *args):
        async with self.session() as s:
            for arg in args:
                if arg:
                    await s.merge(arg)
            await s.commit()

    @property
    def user(self):
        return UserGateway(self.session)


class UserGateway(BaseGateway):
    async def get_by_chat_id(self, chat_id: int) -> User:
        async with self.session() as s:
            user = await s.get(User, chat_id)
        return user

    async def create(self, chat_id: int, crypto_pairs: list) -> User:
        async with self.session() as s:
            user = await s.merge(User(id=chat_id, crypto_pairs=crypto_pairs))
            await s.commit()
        return user

    async def get_all_users(self) -> typing.Iterable[User]:
        async with self.session() as s:
            users = await s.execute(select(User))
        return users.scalars()
