import time

import redis
from flask import Flask
from rq import Queue, Connection
import sys

app = Flask(__name__)
# q = Queue(connection=redis.Redis(host='redis', port=6379))
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    print('**** get_hit_count(), ', file=sys.stderr)
    while True:
        try:
            print('*** In While True (hit) ', file=sys.stderr)
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    print('In hello', file=sys.stderr)
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)



@app.route('/tasks', methods=["POST", "GET"])
def run_task():
    with Connection(redis.Redis(host='redis', port=6379)):
        q = Queue()
        job = q.enqueue(get_hit_count)
        print('** In queue...', file=sys.stderr)
        response_object = {
            "status": "success",
            "data": {
                "task_id": job.get_id()
            }
        }
    print('**\n The response Object is:\n', file=sys.stderr)
    print(response_object, file=sys.stderr) 
    return response_object


@app.route('/tasks/<id>', methods=["POST", "GET"])
def get_task(id):
    with Connection(redis.Redis(host='redis', port=6379)):
        q = Queue()
        print('** Fetching_job id...\n, NOW IS SUPPOSE TO APPEAR "get_hit_count()"', file=sys.stderr)
        task = q.fetch_job(id)
        print('** Fetched_job id...', file=sys.stderr)
        if task:
            response_object = {
                "status": "success",
                "data": {
                    "task_id": task.get_id(),
                    "task_status": task.get_status(),
                    "task_result": task.result,
                },
            }
            return response_object
        else:
            return 'ERROR !! --> Task is empty'

