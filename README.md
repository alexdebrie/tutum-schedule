## Tutum Schedule

A minimalistic image to handle scheduling  processes as Tutum Services

### Introduction

I had a number of ETL-like jobs and background processes that needed to
run on varying schedules. I was running each process in its own Docker container
and using `cron` to start the process when it was required. However, this
method was error-prone. Running `cron` in a Docker container requires careful
configuration and can create problems that are be difficult to debug. Further,
the longer you run a container, the more issues you face regarding inconsistent
environments, exactly the issue you're trying to avoid by using Docker.

As a response, I created this Tutum Schedule Dockerfile and utility functions
to help manage scheduling Docker containers. To use it, set up your own
configuration in `tutum-schedule.py`. Deploy it as its own Service on
[Tutum](www.tutum.co) and stop worrying about your background processes.


### Usage

Tutum Schedule relies on the awesome Python [schedule](https://github.com/dbader/schedule)
package created by `dbader`. It implements a simple, Pythonic interface to
schedule tasks.

Examples from the docs:

    def job():
        print("I'm working...")

    schedule.every().day.at("10:30").do(job)
    schedule.every().monday.do(job)

In `tutum-schedule.py.sample`, I've provided a sample script to deploy with
for your own jobs. In addition to a few example schedule jobs, I've also
provided two helper functions:

* __start_service(uuid)__: used for restarting stopped services that are
saved in your Tutum account;
* __create_service(**kwargs)__: used for creating a new service in your Tutum
account. `create_service()` takes any of the [parameters](https://docs.tutum.co/v2/api/?python#create-a-new-service)
listed in the Tutum API documentation for creating a service.

__Notes__:

* The `schedule` package [runs jobs serially](https://github.com/dbader/schedule/blob/master/FAQ.rst#how-to-execute-jobs-in-parallel).
This shouldn't be a problem here, as the time to make a Tutum API call is
pretty minimal. However, if you put a longer-running function in your job,
it could cause issues.
* Be sure you're using the correct function out of `start_service` and
`create_service`. For `start_service`, the target Service should already be
created and save (but not Running!) in your Tutum account. For `create_service`,
the target Service should exist yet, and you will need to pass all the
necessary parameters for your Service to be created properly. This includes
environment variables, container links, and run command.

### Deploy

To deploy this to Tutum, create your own `tutum-schedule.py` with your
desired configuration. Once you're ready, run:

    docker build -t tutum.co/<username>/<image_name> .
    docker push tutum.co/<username>/<image_name>

Go to your Tutum account and deploy the Service. __Be sure to assign the
`global` role to the Service so it can use the Tutum API on your behalf.__
Be sure to turn on __AutoRestart__ to __Always__ in Tutum for your service just in case python dies.
