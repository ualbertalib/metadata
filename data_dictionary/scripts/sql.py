import json
import mysql.connector
from mysql.connector import Error
from hydraNorth import hydraNorth
from secret import db

def main():
	conn = connect()
	cursor = conn.cursor()
	createDB(cursor)
	cursor.close()
	conn.close()

def createDB(cursor):
	for profileType in ['collection', 'generic', 'thesis']:
		filename = '../profiles/%s/profile.json'
		with open(filename, 'w+') as data:
			for item in json.load(data):
				query = "INSERT INTO %s SET uri='%s';" % (profileType, data['item']['uri'])
				cursor.execute(query)
				for instance in data['item']['acceptedValues']:
					query = "INSERT INTO instances VALUES ('%s', '%s')" % (instance['uri'], instance['label'])
					cursor.execute(query)
					query = "INSERT INTO instanceMap VALUES('%s', '%s')" % (instance['uri'], data['item']['uri'])
					cursor.execute(query)

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(db)
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    main()
