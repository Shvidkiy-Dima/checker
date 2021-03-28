from logging import getLogger

logger = getLogger(__name__)


class SerializerMapMixin:
    serializer_map = dict()

    def get_serializer_class(self):

        serializer_class = self.serializer_map.get(self.request.method.lower())
        if serializer_class is not None:
            return serializer_class

        all_items = list(self.serializer_map.values())
        if not all_items:
            raise ValueError('You must set serializer class into serializer_map')

        logger.warning(f'View {self} doesnt have serializer for {self.request.method} method')

        return all_items.pop()
