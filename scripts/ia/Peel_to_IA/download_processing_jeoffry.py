import tarfile, os, sys, linecache
import shutil
import subprocess
import mysql.connector
from mysql.connector import Error
from Processing import *
from Process_factory import *
from Util import *

#============================
#phrase arguments
#============================
try:
	code=sys.argv[1]
	start_year=sys.argv[2]
	end_year=sys.argv[3]
except:
	print("Usage: Python down_processing.py [newpaper_code] [start_year] [end_year]")
	sys.exit(1)

#=============================
#connect database process
#=============================
try:
	print("Connecting the database")
	#mySQLconnection = mysql.connector.connect(host='127.0.0.1',database='peel_blitz',user='root',password='alberta')
	mySQLconnection = mysql.connector.connect(host='mysql.library.ualberta.ca',database='peel_blitz',user='peel',password='password')
	#sql_select_Query = "select * from newspapers where newspaper='{}' and noid is not NULL and year between {} and {}".format(code, start_year, end_year)
	sql_select_Query = "select * from newspapers where newspaper='{}' and year=1919 and month=5 and day=28 and noid is not NULL".format(code)
	print(sql_select_Query)
	cursor = mySQLconnection .cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	print("Total number of rows in python_developers is - ", cursor.rowcount)
	print ("Printing each row's column values i.e.  developer record")
	for row in records:
		#get noid
		open_noid=row[1]
		#download to temp folder
		print("Starting download noid:",opennoid)
		#swift download newspapers --prefix dig6v6j -D temp
		subprocess.run(["swift", "download","newspapers", "--prefix","#{open_noid}","-D","temp"])
		#upload to IA
		print("Uploading to IA")
		for index, dir in enumerate(os.listdir('temp')):
			#if os.path.isdir(dir):
			path = 'temp/%s' %(dir)
			print ('%s strat processing %s' %(index+1, path))
			make_process_folder(path)
			metadata_obj = metadata(path, code)
			metadata_obj.untar_mets_alto()
			top_mods = metadata_obj.get_mods()
			metadata_process = metadata_obj.get_mets_data()
			item_id = metadata_process[0]
			meta = metadata_process[1]
			image_obj = images(path, item_id)
			image = image_obj.generate_tar()
			uplaod_obj = file_uplaod(path, item_id, meta, log)
			uplaod = uplaod_obj.upload_to_IA()
			print ('Upload finish, updating database record')
		    # update database
			update_Query = "UPDATE newspapers set internet_archive_ark_id = '#{item_id}' where newspaper = 'VCA' and noid = '#{open_noid}'"
			print("This is updating query",update_Query)
			cursor.execute(sql_select_Query)
			# delete temp folder
			shutil.rmtree('temp')





	cursor.close()

except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    # closing database connection.
    if(mySQLconnection .is_connected()):
        mySQLconnection.close()
        print("MySQL connection is closed")
