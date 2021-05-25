from OpenDrive.db import rq


@rq.job('low', timeout=60)
def add(x, y):
    return x + y
