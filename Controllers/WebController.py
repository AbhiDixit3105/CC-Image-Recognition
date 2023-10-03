from flask_apscheduler import APScheduler
from ScalingController import ScalingController
from flask import Flask, request, render_template
import os

# Flask constructor takes the name of
# current module (__name__) as argument.
flask_scheduler = APScheduler()
app = Flask(__name__)
flask_scheduler.init_app(app)
flask_scheduler.start()
sc = ScalingController()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
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
            file.save(filename)
            return "File uploaded successfully"

    return render_template("upload.html")


#@flask_scheduler.task('interval', id='initiateScaling', seconds=10)
def initiateScaling():
    sc.monitor_queue_status()


# main driver function
if __name__ == '__main__':
    app.run()
