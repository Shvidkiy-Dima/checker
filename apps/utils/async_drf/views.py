import asyncio
from rest_framework.views import APIView
from asgiref.sync import sync_to_async


class AsyncApiView(APIView):

    @classmethod
    def as_async_view(cls, *args, **initkwargs):
        view = super().as_view(*args, **initkwargs)

        async def async_view(*args, **kwargs):
            return await view(*args, **kwargs)

        async_view.csrf_exempt = True
        return async_view

    async def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            await sync_to_async(self.initial)(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            if not asyncio.iscoroutinefunction(handler):
                handler = sync_to_async(handler)

            response = await handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def handle_serializer(self, serializer):
        raise NotImplementedError
