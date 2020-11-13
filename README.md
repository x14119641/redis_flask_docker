# How Do I create queue tasks with redis, flask and docker?
I had followed the basic example from:
https://docs.docker.com/compose/gettingstarted/

And tried to build tasks according this other example:
https://testdriven.io/blog/asynchronous-tasks-with-flask-and-redis-queue/

But I don't see that my jobs on the queue are run in the back.
The workflow of this applications is suppose to work like:

1)
* A job is is added in queue in the endpoint:
* `localhost://5000/tasks`
* Returns json with job.status and job.id

2)
* The endpoint:
* `localhost://5000/tasks/<job_id>`
* It is suppose to recive the number of clicks,
* But instead the result returned is None,  seems that the job is never "fetched" from the queue.

# Usage:
`docker-compose up --build`
