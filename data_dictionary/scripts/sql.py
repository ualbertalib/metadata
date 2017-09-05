import json
import mysql.connector
from mysql.connector import Error
from hydraNorth import hydraNorth
from secret import host, database, user, password

def main():
	conn = mysql.connector.connect(host = host, database = database, user = user, password = password)
	cursor = conn.cursor()
	with open('../profiles/generic/profile.json', 'r') as data:
		data = json.load(data)
		for item in data:
			generic = "INSERT INTO generic SET uri='%s';" % (item['uri'])
			collection = "INSERT INTO collection SET uri='%s';" % (item['uri'])
			thesis = "INSERT INTO thesis SET uri='%s';" % (item['uri'])
			print(generic)
			print(collection)
			print(thesis)
			cursor.execute(generic, collection, thesis)
			conn.commit()
			for instance in item['config']['acceptedValues']:
				instances = "INSERT INTO instances VALUES ('%s', '%s');" % (instance['uri'], instance['label'])
				instanceMappings = "INSERT INTO instanceMap VALUES('%s', '%s');" % (instance['uri'], item['uri'])
				print(instances)
				print(instanceMappings)
				cursor.execute(instances, instanceMappings)
				conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
    main()
