import os
import json
from unittest import result
from flask import Flask, jsonify, render_template, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import CableCounter as cc

UPLOAD_FOLDER = os.path.join('web_interface', 'uploaded_by_user') 
ALLOWED_EXTENSIONS= {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

SECRET_KEY = 'flask-session-insecure-secret-key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            
            data = cc.get_cable_number(cc.get_data_pdf(filename))
                        
            if os.path.exists(filename):
                os.remove(filename)
            else:
                print("The file does not exist")
            
            return render_template('result.html', jsonfile=data)
    else:
        return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/result')
def show_result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)    