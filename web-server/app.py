from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Set the directory where uploaded images will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
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

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)