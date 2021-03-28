from typing import Dict
from multiprocessing.pool import Pool, AsyncResult
import django
import os
import sys
import pathlib

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


from background_service.workers.base import BaseWorker
from background_service.workers.http_worker import HttpWorker
from background_service.workers.check_html_worker import HtmlCheckWorker
import asyncio
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',)

logger = logging.getLogger(__name__)


class Runner:

    # workers = [{'name': HttpWorker, 'cpu': 3}, {'name': HtmlCheckWorker, 'cpu': 2}]
    workers = {HttpWorker, HtmlCheckWorker}

    @classmethod
    def start_loop(cls):
        logger.info('Start Runner Loop')
        processes: Dict[BaseWorker: AsyncResult] = {}
        with Pool(processes=os.cpu_count()) as pool:
            while True:
                workers = cls._get_workers(processes)
                for worker in workers:
                    instance = worker()
                    processes[worker] = pool.apply_async(cls._run_service, args=(instance,))

    @classmethod
    def _run_service(cls, service: BaseWorker):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service.run()

    @classmethod
    def _get_workers(cls, processes):
        return [worker for worker in cls.workers
                if not processes.get(worker, False) or processes[worker].ready()]


if __name__ == '__main__':
    Runner.start_loop()
