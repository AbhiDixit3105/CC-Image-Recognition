# from flask import Flask
# import ScalingController
# from flask_apscheduler import APScheduler
# app = Flask(__name__)
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
# sc = ScalingController
#
# class WebController:
#     def __int__(self):
#
#         pass
#
#     @scheduler.task('interval', id='my_job', seconds=10)
#     def initiateScaling(self):
#         sc.monitor_queue_status()
#
#     def run(self):
#         app.run()
# if __name__ == '__main__':
#     wc=WebController()
#     wc.run()