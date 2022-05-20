import subprocess
import os
from unittest import result
from flask import Flask, jsonify, render_template, flash, request, redirect, send_from_directory, json
from numpy import int64
from werkzeug.utils import secure_filename
from backend import CableCounter as cc
from backend.parsedbaudioxml import ParserDBAudioSpeakerXML

SECRET_KEY = "4800188e5667c9fe099638602cd209752bd8a01bf7a5dc3c53aaa6d5afcce214"
UPLOAD_FOLDER = os.path.join('uploaded_by_user') 
ALLOWED_EXTENSIONS= {'pdf', 'csv', 'xlsx', 'dbea', 'dbep', 'dbesa', 'dbacv'}


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 500 * 1000
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
application.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_pdf' not in request.files and "anchor_file" not in request.files:
            flash('Both files not found in request')
            return redirect(request.url)
        
        file_pdf = request.files['file_pdf']
        file_anchor = request.files['file_anchor']

        if file_pdf.filename == '' or file_anchor.filename =='':
            flash('No selected files')
            return redirect(request.url)
        
        if file_pdf and allowed_file(file_pdf.filename) and file_anchor and allowed_file(file_anchor.filename):
            data = process_pdf_csv_files(file_pdf, file_anchor)
            
            return render_template('result.html', jsonfile=json.dumps(data))
    else:
        return render_template('index.html')


@application.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(application.config["UPLOAD_FOLDER"], name)


@application.route('/result')
def show_result():
    return render_template('result.html')


def process_pdf_csv_files(file_pdf, file_anchor):
    filename_pdf = secure_filename(file_pdf.filename)
    filename_anchor = secure_filename(file_anchor.filename)
            
    filename_pdf = os.path.join(application.config['UPLOAD_FOLDER'], filename_pdf)
    filename_anchor = os.path.join(application.config['UPLOAD_FOLDER'], filename_anchor)

    file_pdf.save(filename_pdf)
    file_anchor.save(filename_anchor)

    data = cc.get_cable_number(cc.get_data_pdf(filepath= filename_pdf, anchors_file_path= filename_anchor))
    if os.path.exists(filename_pdf):
        os.remove(filename_pdf)
    else:
        print("The file does not exist")
    return data


if __name__ == "__main__":
    application.run(debug=True)    