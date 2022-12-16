from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from database.api.gateways import Gateway


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, session):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        data['gateway'] = Gateway(self.session)

    async def post_process(self, obj, data, *args):
        del data['gateway']
