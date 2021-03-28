from django.conf import settings


def run_task(task, *args, **kwargs):
    queue = kwargs.pop('queue', None)
    if settings.USE_CELERY:
        task.apply_async(args=args, kwargs=kwargs, queue=queue)
    else:
        task(*args, **kwargs)
