from .. import celery

@celery.task()
def log(msg):
    return msg