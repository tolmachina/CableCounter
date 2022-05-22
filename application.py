import os
from flask import Flask, render_template, flash, request, redirect, send_from_directory, json
from numpy import int64
from werkzeug.utils import secure_filename
from backend import CableCounter as cc

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
        if 'file_speaker' not in request.files and "anchor_file" not in request.files:
            flash('Both files not found in request')
            return redirect(request.url)
        
        file_speaker = (request.files['file_speaker'])
        file_anchor = (request.files['file_anchor'])

        if file_speaker.filename == '' or file_anchor.filename =='':
            flash('No selected files')
            return redirect(request.url)
        
        if file_speaker and allowed_file(file_speaker.filename) and file_anchor and allowed_file(file_anchor.filename):
        
            data = process_files(file_speaker, file_anchor)
            
            return render_template('result.html', jsonfile=json.dumps(data))
    else:
        return render_template('index.html')


@application.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(application.config["UPLOAD_FOLDER"], name)


@application.route('/result')
def show_result():
    return render_template('result.html')

def process_files(speaker_file, anchor_file):
    

    def process_dbea_csv_files(file_dbea, file_anchor):
                
        filename_speaker = os.path.join(application.config['UPLOAD_FOLDER'], file_dbea.filename)
        filename_anchor = os.path.join(application.config['UPLOAD_FOLDER'], file_anchor.filename)

        file_dbea.save(filename_speaker)
        file_anchor.save(filename_anchor)

        processed_speaker_file = cc.get_data_dbea(filepath= filename_speaker, anchors_file_path= filename_anchor)

        data = cc.get_cable_number(processed_speaker_file)
        if os.path.exists(filename_speaker):
            os.remove(filename_speaker)
        else:
            print("The file does not exist")
        return data


    def process_pdf_csv_files(file_pdf, file_anchor):
        filename_pdf = os.path.join(application.config['UPLOAD_FOLDER'], file_pdf)
        filename_anchor = os.path.join(application.config['UPLOAD_FOLDER'], file_anchor)

        file_pdf.save(filename_pdf)
        file_anchor.save(filename_anchor)

        data = cc.get_cable_number(cc.get_data_pdf(filepath= filename_pdf, anchors_file_path= filename_anchor))
        if os.path.exists(filename_pdf):
            os.remove(filename_pdf)
        else:
            print("The file does not exist")
        return data
    
    speaker_filename = secure_filename(speaker_file.filename)
    anchor_filename = secure_filename(anchor_file.filename)
    if speaker_filename.lower().endswith('.pdf'):
        process_pdf_csv_files(speaker_file, anchor_file)
    elif speaker_filename.lower().endswith('.dbea'):
        process_dbea_csv_files(speaker_file, anchor_file)
    else:
        flash('Wrong file extension')
        raise ValueError('Wrong file extension')


if __name__ == "__main__":
    application.run(debug=True)    