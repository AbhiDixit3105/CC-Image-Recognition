import time
from flask_apscheduler import APScheduler
from ScalingController import ScalingController
from flask import Flask, request, render_template, session
from AwsController import AwsController
import os
import boto3
import logging

flask_scheduler = APScheduler()
app = Flask(__name__)
flask_scheduler.init_app(app)
flask_scheduler.start()
app.secret_key = 'cloud_computing_project_Image_Classification'
sc = ScalingController()
awsc = AwsController()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ssm_client = boto3.client('ssm', region_name='us-east-1')
command = 'python app_tier/image_classification.py '
commands = [command]
instance_ids = ['i-013adb440154a55d0']

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# i-02d039e7f2ee6aa41

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/classify', methods=['POST'])
def upload_image_workload():
    
    if request.method == 'POST':
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())
        response_receieved = False
        if request.method == 'POST':
            # Check if a file was uploaded
            if 'myfile' not in request.files:
                return "No file part"
            file = request.files['myfile']

            # Check if the file is empty
            if file.filename == '':
                return "No selected file"

            # Check if the file has an allowed extension
            if not allowed_file(file.filename):
                return "Invalid file extension"

            # If everything is okay, save the file to the uploads folder
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                awsc.upload_to_s3(file)
                response = awsc.send_to_sqs(file.filename)
                while not response_receieved:
                    output_val=awsc.receive_from_sqs()
                    print(output_val)
                    if len(output_val) > 0 :
                        awsc.delete_message(output_val[1])
                        return output_val[0],200
                    time.sleep(2)
        return "No File",400

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        session['results'] = []
    
    if request.method == 'POST':
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())
        response_receieved = False
        if request.method == 'POST':
            # Check if a file was uploaded
            if 'file' not in request.files:
                return "No file part"
            file = request.files['file']

            # Check if the file is empty
            if file.filename == '':
                return "No selected file"

            # Check if the file has an allowed extension
            if not allowed_file(file.filename):
                return "Invalid file extension"

            # If everything is okay, save the file to the uploads folder
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                awsc.upload_to_s3(file)
                response = awsc.send_to_sqs(file.filename)
                while not response_receieved:
                    output_val=awsc.receive_from_sqs()
                    print(output_val)
                    if len(output_val) > 0 :
                        input_string = output_val[0].split(',')
                        result = {'name' : input_string[0] , 'classification' : input_string[1]}
                        results = session.get('results', [])
                        results.append(result)
                        session['results'] = results
                        awsc.delete_message(output_val[1])
                        time.sleep(1)
                    else:
                        response_receieved = True

    return render_template("upload.html",results=session.get('results', []))


@flask_scheduler.task('interval', id='initiateScaling', seconds=15, max_instances=1)
def initiate_scaling():
    print("Monitoring Queues Start")
    sc.monitor_queue_status()
    print("Monitoring Queues End")


# main driver function
if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)
