from mysql.connector import connect
import datetime, time
from random import randint
import subprocess
from uuid import uuid4
import os, sys, csv
from Processing import metadata, images, file_upload
from Util import make_process_folder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from secret_info import *

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
language_abbrev_map = {"en": "english", "fr": "french"}
python_print = print
update_query_file = "update_query.sql"
skip_log_file = "skip_log"

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
"""
Spreadsheep must have following columns
row number: indicate the row number of the current row
code: the item code
noid: the download noid
IA URL: could be empty
title: could be empty

Optional column:
MODS: the metadata. If this column does not exist, use code for metadata
newspaper: If this column exist, identify the upload as newspaper uploads
"""
sheet = client.open("Peel backlog - WFL & GAT (29) ").sheet1
IA_col_num = 9
title_col_num = 10
infile_name = "newspaper29.csv" # Depreciated
upload_name = "Postcard"
swift_container = "peel"
update_metadata_only = False
postcards = False


def print(*objects, sep=' ', end='\n', file=sys.stdout, color=(), fit_len=-1):
	line = "".join(map(str, objects))
	fit_len = max(fit_len - len(line), 0)

	for c in color:
		if len(objects) > 1:
			objects = (f"\033[{c}m{objects[0]}",) + objects[1:-1] + (
				f"{objects[-1]}{' ' * fit_len}\033[0m",)
		elif len(objects) == 1:
			objects = (f"\033[{c}m{objects[0]}{' ' * fit_len}\033[0m",)
	python_print(*objects, sep=sep, end=end, file=file)


def test():
	while True:
		temp_folder = f"/mnt/peeldata/ddev/temp_{uuid4()}"
		if not os.path.isdir(temp_folder):
			os.mkdir(temp_folder)
			break

	# Uncomment this for database usage
	'''
	# Get noids
	cnx = connect(host=db_host, database=db, user=db_username, password=db_password, port=db_port, charset='utf8', use_pure=True)

	cursor = cnx.cursor()
	query = (f"SELECT noid, newspaper, year, month, day, language"
				f"  FROM {db}.newspapers"
				f" WHERE newspaper IN {codes} AND"
				f"       noid IS NOT NULL AND"
				f"       internet_archive_ark_id IS NULL;")

	cursor.execute(query)
	result = cursor.fetchall()
	cursor.close()
	'''

	result = list()
	with open(infile_name, 'r') as file:
		infile = csv.DictReader(file)
		for row in infile:
			new_row = {key.strip(): value.strip() for key, value in row.items()}
			new_row["upload name"] = upload_name
			result.append(new_row)
			# result.append([row["noid"].strip(), upload_name, row["MODS"].strip(), row["row number"].strip(), row["Code"].strip()]) # Depreciated

	if len(sys.argv) >= 4 and sys.argv[-3] == "-range":
		result = result[int(sys.argv[-2]):int(sys.argv[-1])]

	# Get existance
	total = len(result)
	exist_noid = []
	if os.path.isfile(update_query_file):
		with open(update_query_file, 'r') as query_file:
			for line in query_file:
				line = line.strip('\n')
				if len(line) > 10:
					exist_noid.append(line[line.rfind('dig'):-2])
		with open(skip_log_file, 'r') as log_file:
			for line in log_file:
				line = line.strip('\n')
				if len(line) != 0:
					exist_noid.append(line.split(',')[0])
	fail_count = 0
	finish_count = 0
	skip_count = 0

	start_time = datetime.datetime.now()
	previous_time = start_time

	with open("log.txt", 'a') as log:
		for row in result:
			try:
				#get noid
				open_noid = row["noid"]
				# if open_noid in exist_noid and not update_metadata_only:# or open_noid[3] == '7':
				if open_noid in exist_noid:
					# print(f"{open_noid} already uploaded or marked as skip file, skip.", color=[94])
					finish_count += 1
					skip_count += 1
					continue
				print(f"                                     ", color=[45])
				print(f"  +-------------------------------+  ", color=[45])
				print(f"  |         Start {open_noid}         |  ", color=[45])
				print(f"  +-------------------------------+  ", color=[45])
				print(f"                                     ", color=[45])
				
				if row.get("MODS"):
					metadata_location = f"/diginit/work/peel/metadata/{row['MODS'][0]}/{row['MODS'][1:3]}/{row['MODS'][3:5]}/{row['MODS']}.xml"
				elif row.get("newspaper"):
					metadata_location = f"/diginit/work/peel/metadata/Q/{row['newspaper']}.xml"
				else:
					metadata_location = f"/diginit/work/peel/metadata/{row['code'][:2]}/{row['code'][2:5]}/{row['code']}.xml"

				if not os.path.isfile(metadata_location):
					metadata_type = "MODS" if row.get("MODS") else "newspaper" if row.get("newspaper") else "code" 
					print(f"Cannot find metadata for {open_noid} in Jeoffry ({row[metadata_type]})", color=[5, 91])
					print(f"Fall back and upload with its own METS", color=[5, 91])
					metadata_location = None

				#download to temp folder
				retry_times = 0
				while True:
					print(f"Starting download noid: {open_noid}", color=[7, 45])
					return_msg = subprocess.run(["swift", *swift_login, "download", swift_container, "--prefix", open_noid, "-D", temp_folder], stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
					lines = return_msg.stdout.decode().split('\n')
					print(return_msg.stdout.decode())
					if "Authorization Failure. Authorization failed: Forbidden (HTTP 403)" != lines[0] and not lines[0].startswith("Container GET failed: "):
						break
					print(f"Retry {retry_times} ...")
					retry_times += 1
					time.sleep(randint(1, 5))

				prefixes = list()
				for line in lines:
					if "Error" in line:
						idx = line.index(open_noid)
						end_quote = line[idx:].index("'")
						prefixes.append(line[idx:idx + end_quote])
				for prefix in prefixes:
					while not os.path.isfile(f"{temp_folder}/{prefix}"):
						subprocess.run(["swift", *swift_login, "download", swift_container, "--prefix", prefix, "-D", temp_folder])

				print("Done")
				# subprocess.run(["swift", "download", swift_container, "--prefix", open_noid, "-D", temp_folder])
				time.sleep(5)

				folders = os.listdir(temp_folder)
				if len(folders) == 0:
					print(f"Cannot locate {open_noid} in Swift", color=[5, 91])
					with open(skip_log_file, 'a') as log_file:
						log_file.write(f"{open_noid}, {row['upload name']}, cannot locate file in Swift\n")
					finish_count += 1
					fail_count += 1
					continue
					
				# print(f"{temp_folder}/{open_noid}/mets")
				if not os.path.isdir(f"{temp_folder}/{open_noid}/mets") and metadata_location is None:
					print(f"Cannot find MODS and METS for {open_noid} in Jeoffry ({row[metadata_type]})", color=[5, 91])
					with open(skip_log_file, 'a') as log_file:
						log_file.write(f"{open_noid}, {row[metadata_type]}, cannot locate MODS and METS file in Jeoffry\n")
					finish_count += 1
					fail_count += 1
					subprocess.run(["rm", "-rf", f"{temp_folder}/{open_noid}"])
					continue

				for i, dir in enumerate(folders):

					#upload to IA
					print(f"Uploading {open_noid} to IA", color=[7, 45])
					path = '%s/%s' %(temp_folder, dir)
					print (f"Start processing {path} ({i + 1}/{len(folders)})")
					make_process_folder(path)
					metadata_obj = metadata(path, row["upload name"], metadata_location)
					metadata_obj.untar_mets_alto()
					top_mods = metadata_obj.get_mods(item=True)
					mets_data = metadata_obj.get_mets_data()
					print(f"top_modes: {top_mods}\n mets_data: {mets_data}")
					if not mets_data:
						print(f"{open_noid} detects legacy METS data", color=[91])
						metadata_obj.set_legacy()
						mets_data = metadata_obj.get_mets_data()
						if not mets_data:
							fail_count += 1
							finish_count += 1
							subprocess.run(["rm", "-rf", path])
							continue

					item_id = mets_data[0]
					print(f"row: {row}")
					if item_id == row.get("MODS") and item_id != row["code"]:
						if not os.path.isdir(f"{temp_folder}/{open_noid}/mets"):
							item_id = row["code"]
					mets = mets_data[1]
					mets[0] = mets[0].strip()
					if mets[0].startswith('[') and mets[0].endswith(']'):
						mets[0] = mets[0][1:-1]
					art = mets_data[2]

					# print(mets, art)

					language_in_mod = None
					if top_mods and len(top_mods) >= 13:
						language_in_mod = top_mods[12]
					ia_metadata = metadata_obj.make_IA_metadata(mets, top_mods, art, item_id, language_in_mod) 
					print(ia_metadata)
					# input("pause")
					image_obj = images(path, item_id)
					image_obj.generate_tar(postcards=postcards)
					upload_obj = file_upload(path, item_id, ia_metadata, log)
					result = upload_obj.upload_to_IA(update_only=update_metadata_only)

					if result:
						print(f"Upload finish, updating database record", color=[100, 92])
						# update database
						# cnx = connect(host=db_host, database=db, user=db_username, password=db_password, port=db_port, charset='utf8', use_pure=True)
						# cursor = cnx.cursor()
						# if not update_metadata_only:
						with open(update_query_file, 'a') as query_file:
							update_Query = f"UPDATE newspapers set internet_archive_ark_id = '{item_id}' where newspaper = '{row['code']}' and noid = '{open_noid}';\n"
							query_file.write(update_Query)
						
						sheet.update_cell(int(row["row number"]), IA_col_num, f"https://archive.org/details/{item_id}")
						sheet.update_cell(int(row["row number"]), title_col_num, f"{mets[0]}")
						if metadata_location is None:
							sheet.update_cell(int(row["row number"]), title_col_num + 1, "MODS file missing, using METS only")
						# print("This is updating query", update_Query)
						# cursor.execute(update_Query)
						# cursor.close()

						# delete temp folder
					else:
						print(f'Upload failed, retry next time', color=[5, 91])
						fail_count += 1
					subprocess.run(["rm", "-rf", path])
				
				if not mets_data:
					continue
			except KeyboardInterrupt:
				break
			except:
				print(f'Upload failed, retry next time', color=[5, 91])
				print(sys.exc_info())
				fail_count += 1
				with open(skip_log_file, 'a') as log_file:
					log_file.write(f"{open_noid}, {row['noid']}, {sys.exc_info()}\n")
				subprocess.run(["rm", "-rf", path])

			finish_count += 1
			current_time = datetime.datetime.now()

			progress = f"{finish_count} out of {total} ({finish_count * 100 / total:.2f}%), {fail_count} failed"
			max_len = len(progress) + 3
			print(f"{'=' * (max_len + 26)}", color=[1, 7, 93])
			print(f"   Current time is:       ", end='', color=[1, 7, 93])
			print(f"{current_time}", color=[7, 93], fit_len=max_len)
			print(f"   Current progress:      ", end='', color=[1, 7, 93])
			print(f"{progress}", color=[7, 93], fit_len=max_len)
			current_run_time = current_time - start_time
			current_progress_perc = (finish_count - skip_count) / (total - skip_count)
			estimate_remain = current_run_time / current_progress_perc - current_run_time
			print(f"   Current total runtime: ", end='', color=[1, 7, 93])
			print(f"{current_run_time}", color=[7, 93], fit_len=max_len)
			print(f"   Last update runtime:   ", end='', color=[1, 7, 93])
			print(f"{current_time - previous_time}", color=[7, 93], fit_len=max_len)
			print(f"   Estimate remaining:    ", end='', color=[1, 7, 93])
			print(f"{estimate_remain}", color=[7, 93], fit_len=max_len)
			print(f"   Estimate finish time:  ", end='', color=[1, 7, 93])
			print(f"{current_time + estimate_remain}", color=[7, 93], fit_len=max_len)
			print(f"{'=' * (max_len + 26)}", color=[1, 7, 93])

			# input("Pause")


			previous_time = current_time


	subprocess.run(["rm", "-rf", temp_folder])


if __name__ == '__main__':
	test()
	# if len(sys.argv) < 2:
	# 	print("Usage: python3 upload_to_ia.py <CODE1> <CODE2> ...")
	# else:
	# 	test(tuple(sys.argv[1:] + [""]))
