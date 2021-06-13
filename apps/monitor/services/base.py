import time
from datetime import timedelta
from django.utils import timezone



async def monitor_first_request(worker, url, method, interval):
    attrs = {}
    async with worker.get_client_session() as session:

        is_error, response, body, response_time \
            = await worker.handle_request(session, url, method=method)

        attrs['last_request'] = timezone.now()
        attrs['next_request'] = timezone.now() + timedelta(seconds=interval)
        attrs['error'] = response if is_error else None
        attrs['response_time'] = response_time
        attrs['response_code'] = response.status if not is_error else None
        attrs['body'] = body

    return attrs
