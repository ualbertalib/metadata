import os
from Bib import main
from time import sleep
from flask import Flask, request, redirect, url_for, send_from_directory, flash, render_template, jsonify
from werkzeug.utils import secure_filename
from pymarc import MARCReader, XmlHandler, record_to_xml, XMLWriter
from os import listdir
import subprocess
from os.path import isfile, join
import lxml.etree as ET

app = Flask(__name__)

urls = (
    '/', 'index',
    '/favicon.ico', 'icon'
)

class icon:
    def GET(self): raise web.seeother("/static/favicon.ico")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print (a, b)
    return jsonify(result=a + b)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

app.run(host='0.0.0.0')