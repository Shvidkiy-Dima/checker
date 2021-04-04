import asyncio
from rest_framework.views import APIView
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


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

    
class AsyncCreateViewMixin(generics.CreateAPIView):

    async def post(self, request, *args, **kwargs):
        await self.start_async_view(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        data, serializer = await self.handle_serializer(serializer)
        data = await self.end_async_view(data, serializer, request, *args, **kwargs)
        return Response(data, status=status.HTTP_201_CREATED)

    @database_sync_to_async
    def handle_serializer(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, serializer

    async def start_async_view(self, request, *args, **kwargs):
        pass

    async def end_async_view(self, data, serializer, request, *args, **kwargs):
        return data
