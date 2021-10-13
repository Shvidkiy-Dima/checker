import time
from datetime import timedelta
from django.utils import timezone


async def monitor_first_request(worker, url, method, interval, max_timeout):
    attrs = {}
    async with worker.get_client_session() as session:

        is_error, body, response_time, response_code  \
            = await worker.handle_request(session, url, method=method, timeout=max_timeout)

        attrs['last_request'] = timezone.now()
        attrs['next_request'] = timezone.now() + timedelta(seconds=interval)
        attrs['error'] = body if is_error else None
        attrs['is_successful'] = is_error
        attrs['response_time'] = response_time
        attrs['response_code'] = response_code

    return attrs
