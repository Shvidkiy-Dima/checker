import time


async def monitor_first_request(monitor, worker):
    async with worker.get_client_session() as session:
        start = time.monotonic()
        error, response = await worker.handle_request(monitor, session)
        response_time = time.monotonic() - start

        if not error:
            data = await worker.handle_response(response, monitor, response_time)
        else:
            data = await worker.handle_error(response, monitor, response_time)

        return data['monitor']
