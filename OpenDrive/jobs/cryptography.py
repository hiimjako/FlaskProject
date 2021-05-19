from rq import job


@job
def process(i):
    print('jobbing')
    print(i)
    #  Long stuff to process
