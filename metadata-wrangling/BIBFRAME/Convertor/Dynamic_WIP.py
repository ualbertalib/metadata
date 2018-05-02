import os
from Bib_F import main, trans
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


'''def upload_file():
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
                return render_template("file_error.html")
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print (filename)
            return redirect(url_for('upload_success', 
                                    filename=filename))
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
    return 
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/_getProperties')
def _getProperties():
    g = request.args.get('g', 0, type=str)
    results = main("1985eresOrigbf.xml")
    result = {'properties': results}
    print (result)
    return jsonify(result=result)

@app.route('/_perf')
def _perf():
    g = request.args.get('g', 0, type=str)
    results = do("1985eresOrigbf.xml")
    result = {'properties': results}
    print (result)
    return jsonify(result=result)

@app.route('/yield')
def index():
    def inner():
        for x in range(100):
            sleep(1)
            yield '%s<br/>\n' % x
    return Response(inner(), mimetype='text/html')

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
        main(file)
        with open(file, "rb") as infile:
            reader = MARCReader(infile, to_unicode=True, force_utf8=False, utf8_handling='ignore')
            files = []
            for record in reader:
                i = 0
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
                    writer = XMLWriter(open('processed/' + 'unknownTitle' + i + '.xml','wb'))
                    files.append('unknownTitle' + i)
                    i += 1

            infile.close()
            print(files)
            xslt = ET.parse("marc2bibframe2-master/xsl/marc2bibframe2.xsl")
            for file in files:
                f = "processed/" + file + ".xml"
                dom = ET.parse(f)
                transform = ET.XSLT(xslt)
                newdom = transform(dom)
                with open ("BIB/" + file + ".xml", "w+") as oo:
                    oo.write(str(newdom).replace('<?xml version="1.0"?>', ''))
        return redirect(url_for('process_success', 
                                    files="files"))
    return 
    <!doctype html>
    <h3>your file {{filename}} was suucessfuly uploaded</h3>
    <form method=post>
      <p><input type=submit value=Proccess>
    </form>
  

@app.route('/process_success/<files>', methods=['GET', 'POST'])
def process_success(files):
    if request.method == 'POST':
        #xslt = ET.parse("marc2bibframe2-master/xsl/marc2bibframe2.xsl")
        #for f in files:
            #f = "processed/" + f + ".xml"
            #print (f)
            #dom = ET.parse(f)
            #transform = ET.XSLT(xslt)
            #newdom = transform(dom)
            #with open ("BIB/" + f + "w+") as oo:
            #    oo.write(str(newdom).replace('<?xml version="1.0"?>', ''))
            d = ''
    return 
    <!doctype html>
    <h3>MARC file {{ filename }} was processed to XML successfully</h3>
    <form method=post>
      <p><input type=submit value=Proccess>
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
