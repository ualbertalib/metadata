#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/zschoenb/Documents/Projects/metadata/data_dictionary/www/Flask/")

from Flask import app as application
application.secret_key = 'test'