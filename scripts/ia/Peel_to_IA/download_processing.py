import tarfile, os, sys, linecache
import mysql.connector
from mysql.connector import Error
from Processing import *
from Process_factory import *
from Util import *

# #============================
# #phrase arguments
# #============================
# try:
# 	code=sys.argv[1]
# 	start_year=sys.argv[2]
# 	end_year=sys.argv[3]
# except:
# 	print("Usage: Python down_processing.py [newpaper_code] [start_year] [end_year]")
# 	sys.exit(1)
#
# #=============================
# #connect database and get noid
# #=============================
# try:
# 	print("Connecting the database")
# 	mySQLconnection = mysql.connector.connect(host='127.0.0.1',database='peel_blitz',user='root',password='alberta')
# 	sql_select_Query = "select * from newspapers where newspaper='{}' and noid is not NULL and year between {} and {}".format(code, start_year, end_year)
# 	print(sql_select_Query)
# 	cursor = mySQLconnection .cursor()
# 	cursor.execute(sql_select_Query)
# 	records = cursor.fetchall()
# 	print("Total number of rows in python_developers is - ", cursor.rowcount)
# 	print ("Printing each row's column values i.e.  developer record")
# 	for row in records:
# 		print("Node =",row[1])
# 	    # print("Id = ", row[0], )
# 	    # print("Name = ", row[1])
# 	    # print("JoiningDate  = ", row[2])
# 	    # print("Salary  = ", row[3], "\n")
# 	cursor.close()
#
# except Error as e :
#     print ("Error while connecting to MySQL", e)
# finally:
#     # closing database connection.
#     if(mySQLconnection .is_connected()):
#         mySQLconnection.close()
#         print("MySQL connection is closed")



#================================
#Download from openstack, need to be test on Jeoffry
import subprocess
subprocess.run(["ls", "-l"])
#================================


#=================================
#upload to IA
#=================================

with open('upload-log.txt', 'a') as log:


	for index, dir in enumerate(os.listdir('Vulcan')):
		try:
			if index < 2500:
				#if os.path.isdir(dir):
				path = 'Vulcan/%s' %(dir)
				print ('%s strat processing %s' %(index+1, path))
				make_process_folder(path)
				metadata_obj = metadata(path)
				metadata_obj.untar_mets_alto()
				metadata_process = metadata_obj.get_mets_data()
				item_id = metadata_process[0]
				meta = metadata_process[1]
				image_obj = images(path, item_id)
				image = image_obj.generate_tar()
				uplaod_obj = file_uplaod(path, item_id, meta, log)
				uplaod = uplaod_obj.upload_to_IA()
				print ('----------------------------------------------------------')
			else:
				break
		except:
			PrintException()
			pass


#==================================
#update database
