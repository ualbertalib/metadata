import os
import time
from datetime import datetime
from Bib import main
from time import sleep
from flask import Flask, Response, request, redirect, url_for, send_from_directory, jsonify, flash, render_template
from werkzeug.utils import secure_filename
from pymarc import MARCReader, XmlHandler, record_to_xml, XMLWriter
from os import listdir
import subprocess
from os.path import isfile, join
import lxml.etree as ET


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'xml', 'mrc'])

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
        file = "uploads/" + filename
        if not os.path.exists("processed"):
            os.makedirs("processed")
        with open(file, "rb") as infile:
            ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
            reader = MARCReader(infile, to_unicode=True, force_utf8=False, utf8_handling='ignore')
            files = []
            for i, record in enumerate(reader):
                print ("converting record number " + str(i) + " to XML")
                if record.title():
                    ti = record.title()
                    ti = ti.replace("/", "")
                    ti = ti.replace(" ", "_")
                    ti = ti[0:50]
                    writer = XMLWriter(open('processed/' + ti + '.xml','wb'))
                    writer.write(record)
                    writer.close()
                    files.append(ti)
                else:
                    writer = XMLWriter(open('processed/' + 'unknownTitle' + str(i) + '.xml','wb'))
                    files.append('unknownTitle' + str(i))
            infile.close()
            #print (file + " was successfully converted to XML")
            xslt = ET.parse("marc2bibframe2-master/xsl/marc2bibframe2.xsl")
            tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
            #print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
            for i, file in enumerate(files):
                #print ("start processing record number " + str(i))
                #print ("starting BIBFRAME transformation")
                f = "processed/" + file + ".xml"
                dom = ET.parse(f)
                transform = ET.XSLT(xslt)
                newdom = transform(dom)
                if not os.path.exists("BIB"):
                    os.makedirs("BIB")
                with open ("BIB/" + file + ".xml", "w+") as oo:
                    oo.write(str(newdom).replace('<?xml version="1.0"?>', ''))
                #print ("starting enrichment process")
                main("BIB/" + file + ".xml")
                tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
                #print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
        return redirect(url_for('process_success', 
                                    files=file))
    return''' 
    <!doctype html>
    <h3>your file {{filename}} was suucessfuly uploaded</h3>
    <form method=post>
      <p><input type=submit value=Proccess>
    </form>'''
  

@app.route('/process_success/<files>', methods=['GET', 'POST'])
def process_success(files):
    if request.method == 'POST':
        print ('')
    return''' 
    <!doctype html>
    <h3>MARC file {{ filename }} was processed to BIBFRAME successfully</h3>
    <form method=post>
      <p><input type=submit value=Enrich>
    </form>
    '''    

'''@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)'''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, passthrough_errors=True)
