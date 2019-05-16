import sys, linecache, os

def make_process_folder(dir):
		directory = str(dir) + "/processing"
		if not os.path.exists(directory):
			os.makedirs(directory)

def PrintException():
    with open ('log_file', "a+") as logs:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))
        logs.write("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))
        logs.write("\n")
