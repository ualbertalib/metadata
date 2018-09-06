import os
import sys
import linecache
from os.path import isfile, join

def clean_up(l):
    for i in list(l):
        if l[i] == []:
            print (i)
            del l[i]
    return l

def PrintException(log_file, error):
    log = 'results/%s/logs/log_file' %(log_file.replace('-error-logs', ''))
    with open (log, "w+") as logs:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("\n")

def clearLogs(log_file, filename):
    folder = 'results/%s/logs' %(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, log_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def clear_files(output):
    folder = 'results/%s/enhanced-files' %(output)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, output)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def clear_TSV(filename):
    folder = 'results/%s/TSVs' %(filename)
    file = 'URIs-' + filename + '.tsv'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def delete_temp():
    try:
        if os.path.isfile('temp-file.xml'):
            os.unlink('temp-file.xml')
    except Exception as e:
        print(e)

def clear_processing():
    folder = 'Processing'
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)