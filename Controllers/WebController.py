from flask_apscheduler import APScheduler
from ScalingController import ScalingController
from flask import Flask

# Flask constructor takes the name of
# current module (__name__) as argument.
flask_scheduler = APScheduler()
app = Flask(__name__)
flask_scheduler.init_app(app)
flask_scheduler.start()
sc = ScalingController()


@app.route('/')
def hello_world():
    return 'Hello World'

@flask_scheduler.task('interval', id='initiateScaling', seconds=10)
def initiateScaling():
    sc.monitor_queue_status()
# main driver function
if __name__ == '__main__':
    app.run()

