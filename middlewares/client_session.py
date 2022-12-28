from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class ClientSessionMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, session):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        data['client_session'] = self.session

    async def post_process(self, obj, data, *args):
        del data['client_session']
