from channels.db import database_sync_to_async
from utils.functions import get_user_by_token


class TokenAuthMiddlewareStack:

    def __init__(self, asgi_app):
        self.app = asgi_app

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string']
        token = self._parse_query_string(query_string)
        scope['user'] = await database_sync_to_async(get_user_by_token)(token)
        return await self.app(scope, receive, send)

    def _parse_query_string(self, query_string):
        _, token = query_string.decode().split('=')
        return token
