from multiprocessing.pool import Pool, AsyncResult
from multiprocessing import Pipe
import json
import os
import sys
import pathlib
import asyncio
import logging
from collections import defaultdict
import django
import numpy as np

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from background_service.fetcher.workers.base import BaseWorker
from background_service.fetcher.workers.http_worker import HttpWorker
from background_service.fetcher.workers.check_html_worker import HtmlCheckWorker


class Runner:
    # Subprocesses per workers
    workers = [{'name': HttpWorker, 'cpu': 3}, {'name': HtmlCheckWorker, 'cpu': 2}]

    @classmethod
    def start_loop(cls):
        amount_processes = sum(w['cpu'] for w in cls.workers)
        with Pool(processes=amount_processes) as pool:
            processes = cls._start_workers(pool)
            cls._listen_workers(processes)

    @classmethod
    def _start_workers(cls, pool: Pool):
        processes = defaultdict(list)
        for worker in cls.workers:
            proc_for_worker = worker['cpu']
            for _ in range(proc_for_worker):
                parent_conn, child_conn = Pipe()
                WorkerKlass = worker['name']
                worker_instance = WorkerKlass()
                proc_params = (parent_conn, pool.apply_async(cls._run_worker, args=(child_conn, worker_instance)))
                processes[WorkerKlass].append(proc_params)

        return processes

    @classmethod
    def _listen_workers(cls, processes):
        while True:
            for worker, proc_params in processes.items():
                print( all(c.poll() for c, _ in proc_params))
                # Check that all sub processes for this worker made job and ready to next chunks
                if all(c.poll() for c, _ in proc_params):
                    chunks_for_worker = len(proc_params)
                    qs = worker.get_monitors().active()
                    print(qs)
                    # split monitors into chunks - example 1200 monitors / 3 workers = 400 monitors per worker
                    monitors = np.array_split(qs.values_list('id', flat=True), chunks_for_worker)

                    for n, (conn, proc) in enumerate(proc_params):
                        conn.recv()
                        conn.send(monitors[n])


    @classmethod
    def _run_worker(cls, conn, service: BaseWorker):
        # Initiate connection with parent process
        conn.send(1)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service.run(conn)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S', )

    logger = logging.getLogger(__name__)

    Runner.start_loop()
