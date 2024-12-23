import time
import redis
from flask import Flask, render_template
import socket

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route("/")
def index():
    count = get_hit_count()
    hostname = socket.gethostname()
    return render_template('index.html', hostname=hostname, count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)