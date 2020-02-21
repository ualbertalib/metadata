from mysql.connector import connect
import datetime, time
import subprocess
from uuid import uuid4
import os, sys
from Processing import metadata, images, file_upload
from Util import make_process_folder

language_abbrev_map = {"en": "english", "fr": "french"}
python_print = print
force = False
swift_login = ["REMOVED"]

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



def test(codes):
	while True:
		temp_folder = "REMOVED" + str(uuid4())
		if not os.path.isdir(temp_folder):
			os.mkdir(temp_folder)
			break

	db_host = "REMOVED"
	db = "REMOVED"
	db_username = "REMOVED"
	db_password = "REMOVED"
	db_port = "REMOVED"
	update_query_file = "update_query.sql"
	skip_log_file = "skip_log"

	# Get noids
	cnx = connect(host=db_host, database=db, user=db_username, password=db_password, port=db_port, charset='utf8', use_pure=True)

	cursor = cnx.cursor()
	query = (f"SELECT noid, newspaper, year, month, day, language"
				f"REMOVED")

	cursor.execute(query)
	result = cursor.fetchall()
	cursor.close()

	if len(sys.argv) >= 5 and sys.argv[-3] == "-range":
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
			#get noid
			open_noid=row[0]
			if open_noid in exist_noid and not force:
				print(f"{open_noid} already uploaded or marked as skip file, skip.", color=[94])
				finish_count += 1
				skip_count += 1
				continue

			#download to temp folder
			print(f"Starting download noid: {open_noid}", color=[7, 45])
			subprocess.run(["swift", *swift_login, "download", "newspapers", "--prefix", open_noid, "-D", temp_folder])
			time.sleep(10)

			folders = os.listdir(temp_folder)
			if len(folders) == 0:
				print(f"Cannot locate {open_noid} in Swift", color=[5, 91])
				with open(skip_log_file, 'a') as log_file:
					log_file.write(f"{open_noid}, {row[1]}, cannot locate file in Swift\n")
				finish_count += 1
				fail_count += 1
				continue
				
			for i, dir in enumerate(folders):
				#upload to IA
				print(f"Uploading {open_noid} to IA", color=[7, 45])
				path = '%s/%s' %(temp_folder, dir)
				print (f"Start processing {path} ({i + 1}/{len(folders)})")
				make_process_folder(path)
				metadata_obj = metadata(path, row[1])
				metadata_obj.untar_mets_alto()
				top_mods = metadata_obj.get_mods()
				mets_data = metadata_obj.get_mets_data()
				if not mets_data:
					print(f"{open_noid} detects legacy METS data", color=[91])
					metadata_obj.set_legacy()
					mets_data = metadata_obj.get_mets_data()
					# fail_count += 1
					# finish_count += 1
					# subprocess.run(["rm", "-rf", path])
					# continue

				item_id = mets_data[0]
				mets = mets_data[1]
				art = mets_data[2]

				ia_metadata = metadata_obj.make_IA_metadata(mets, top_mods, art, item_id, row[5]) 
				image_obj = images(path, item_id)
				image_obj.generate_tar()
				upload_obj = file_upload(path, item_id, ia_metadata, log)
				result = upload_obj.upload_to_IA(update_only=force)

				if result:
					print(f"Upload finish, updating database record", color=[100, 92])
					# update database
					# cnx = connect(host=db_host, database=db, user=db_username, password=db_password, port=db_port, charset='utf8', use_pure=True)
					# cursor = cnx.cursor()
					if not force:
						with open(update_query_file, 'a') as query_file:
							update_Query = "UPDATE newspapers set internet_archive_ark_id = '%s' where newspaper = '%s' and noid = '%s';\n" % (item_id, row[1], open_noid)
							query_file.write(update_Query)
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


			previous_time = current_time


	subprocess.run(["rm", "-rf", temp_folder])


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python3 upload_to_ia.py <CODE1> <CODE2> ...")
	else:
		test(tuple(sys.argv[1:] + [""]))
