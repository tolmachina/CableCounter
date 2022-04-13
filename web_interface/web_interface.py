import subprocess
import os
from unittest import result
from flask import Flask, jsonify, render_template, flash, request, redirect, send_from_directory, json
from werkzeug.utils import secure_filename
import CableCounter as cc

SECRET_KEY = "4800188e5667c9fe099638602cd209752bd8a01bf7a5dc3c53aaa6d5afcce214"
UPLOAD_FOLDER = os.path.join('web_interface', 'uploaded_by_user') 
ALLOWED_EXTENSIONS= {'pdf', 'csv', 'xlsx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        if 'file_pdf' not in request.files and "anchor_file" not in request.files:
            flash('Both files not found in request')
            return redirect(request.url)
        
        file_pdf = request.files['file_pdf']
        file_anchor = request.files['file_anchor']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file_pdf.filename == '' or file_anchor.filename =='':
            flash('No selected file')
            return redirect(request.url)
        
        if file_pdf and allowed_file(file_pdf.filename) and file_anchor and allowed_file(file_anchor.filename):
            filename_pdf = secure_filename(file_pdf.filename)
            filename_anchor = secure_filename(file_anchor.filename)
            
            filename_pdf = os.path.join(app.config['UPLOAD_FOLDER'], filename_pdf)
            
            filename_anchor = os.path.join(app.config['UPLOAD_FOLDER'], filename_anchor)

            file_pdf.save(filename_pdf)
            file_anchor.save(filename_anchor)
            
            print(filename_anchor)
            print(filename_pdf)

            data = cc.get_cable_number(cc.get_data_pdf(filepath= filename_pdf, anchors_file_path= filename_anchor))

            if os.path.exists(filename_pdf):
                os.remove(filename_pdf)
            else:
                print("The file does not exist")
            print("DATA\n", data)
            return render_template('result.html', jsonfile=json.dumps(data))
    else:
        return render_template('index.html')

# @app.route('/upload_anchor', methods=['GET', 'POST'])
# def upload_anchor_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filename)
            

                        
#             if os.path.exists(filename):
#                 os.remove(filename)
#             else:
#                 print("The file does not exist")
            
#             return render_template('result.html', jsonfile=data)
#     else:
#         return render_template('index.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/result')
def show_result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)    