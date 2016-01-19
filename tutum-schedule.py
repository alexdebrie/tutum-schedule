import functools
import schedule
import time
import tutum

def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
    return wrapper

@catch_exceptions
def start_service(uuid):
    """
    Wrapper function to start a stopped Tutum Service by its UUID.
    """
    service = tutum.Service.fetch(uuid)
    service.start()

@catch_exceptions
def create_service(**kwargs):
    """
    Wrapper function to create a new Tutum Service.

    For possible parameters, see https://docs.tutum.co/v2/api/?python#create-a-new-service.
    """
    service = tutum.Service.create(**kwargs)
    service.save()
    service.start()

if __name__ == "__main__":
    """
    Add your own scheduled jobs here.
    See https://github.com/dbader/schedule for schedule syntax.

    Examples:

    If you have already created a Service on Tutum with the UUID of 
    '2463a0c3-bacd-4195-8493-bcbb49681f4a', you can start it every
    hour with:
    schedule.every().hour.do(start_service, '2463a0c3-bacd-4195-8493-bcbb49681f4a')

    If you would like to create a Service to be run every day at 2:15 AM, set
    the schedule with:
    schedule.every(5).day.at("2:15").do(create_service, 
                                        image='tutum.co/user/my-job', 
                                        name='created',
                                        autodestroy="ALWAYS")
    """

    while True:
        schedule.run_pending()
        time.sleep(1)
