import sys
from typing import List, Union
from channels.db import database_sync_to_async
from utils.functions import get_user_by_token
from django.db import connection
from django.conf import settings



class TokenAuthMiddlewareStack:
    """
    Auth via token in subprotocol
    """

    def __init__(self, asgi_app):
        self.app = asgi_app

    async def __call__(self, scope, receive, send):
        subprotocols = scope['subprotocols']
        token = self._parse_subprotocols(subprotocols)
        scope['user'] = await database_sync_to_async(get_user_by_token)(token)
        return await self.app(scope, receive, send)

    def _parse_subprotocols(self, subprotocols: List[str]) -> Union[str, None]:
        tokens = [t.lstrip('token=') for t in
                 filter(lambda s: s.startswith('token='), subprotocols)
                 ]
        return tokens[0] if len(tokens) > 0 else None


class QueryCountMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            start = len(connection.queries)

            response = self.get_response(request)

            summary = len(connection.queries) - start
            sys.stderr.write(f'\nDB requestss {summary}\n')

        else:
            response = self.get_response(request)

        return response
