from typing import Dict
from multiprocessing.pool import Pool, AsyncResult
from multiprocessing import Pipe
import django
import os
import sys
import pathlib

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


from background_service.workers.base import BaseWorker
from background_service.workers.http_worker import HttpWorker
from background_service.workers.check_html_worker import HtmlCheckWorker
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',)

logger = logging.getLogger(__name__)


class Runner:

    # workers = [{'name': HttpWorker, 'cpu': 3}, {'name': HtmlCheckWorker, 'cpu': 2}]
    workers = {HttpWorker, HtmlCheckWorker}


    @classmethod
    def start_loop_safe_mode(cls):
        logger.info('Start Runner Loop')
        processes: Dict[BaseWorker: AsyncResult] = {}
        with Pool(processes=os.cpu_count()) as pool:
            while True:
                workers = cls._get_workers(processes)
                for worker in workers:
                    instance = worker()
                    processes[worker] = pool.apply_async(cls._run_service, args=(instance,))

    @classmethod
    def _get_workers(cls, processes):
        return [worker for worker in cls.workers
                if not processes.get(worker, False) or processes[worker].ready()]

    @classmethod
    def start_loop(cls):
        logger.info('Start Runner Loop')
        with Pool(processes=len(cls.workers)) as pool:
            for worker in cls.workers:
                instance = worker()
                pool.apply_async(cls._run_service, args=(instance,))


    def test_loop(self):
        processes = defaultdict(list)
        with Pool(processes=sum(i['cpu'] for i in self.workers)) as pool:
            for worker in self.workers:

                for i in range(worker['cpu']):
                    parent_conn, child_conn = Pipe()
                    processes[worker['name']].append((parent_conn, pool.apply_async(self._run_service, args=(child_conn,))))

            while True:
                for worker in self.workers:
                    if all(p.poll() and p.recv() in ['done', 'start'] for p in processes[worker['name']]):
                        for c, p in processes[worker['name']]:
                            qs = worker['name'].get_monitors()
                            c.send([])



    @classmethod
    def _run_service(cls, service: BaseWorker, safe=False):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service.run() if safe else service.run_forever()


if __name__ == '__main__':
    Runner.start_loop()
