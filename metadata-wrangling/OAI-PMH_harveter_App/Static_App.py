import os
import time
from datetime import datetime
from time import sleep
from flask import Flask, Response, request, redirect, url_for, send_from_directory, jsonify, flash, render_template
from werkzeug.utils import secure_filename
from os import listdir
import subprocess
from os.path import isfile, join


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'test'

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
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.unlink(file_path)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print (filename)
            return redirect(url_for('upload_success', 
                                    filename=filename))
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
    return''' 
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print ("ddddddddddddd")
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload_success/<filename>', methods=['GET', 'POST'])
def upload_success(filename):
    if request.method == 'POST':
        return redirect(url_for('upload_file'))
    return''' 
    <!doctype html>
    <h3>your file was suucessfuly uploaded</h3>
    <form method=post>
      <p><input type=submit value=Back>
    </form>'''
  

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, passthrough_errors=True)
