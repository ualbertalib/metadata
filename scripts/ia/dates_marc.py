
from os import listdir
from os.path import isfile, join
import pymarc
import json


def main():
	mypath = "/home/zschoenb/Documents/Projects/metadata/metadata-wrangling/internet_archive_coll/albertagovernmentpublications/marc/"
	output = []
	for filename in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
		with open(join(mypath, filename), 'rb') as xml:
			reader = pymarc.marcxml.parse_xml_to_array(xml)
			# a place to store the fieldData
			fileData = {
						'filename': filename,
						'260': [],
						"264": [],
						}

			for record in reader:
				# iterate over all desired fields (each one represents one of the arrays in fieldData)


				for fieldNum in ['260', "264"]:
					# if the desired field exists in this marc record, access it
					if fieldNum in record:
						# iterate over the subfield in this field
						for field in record.get_fields(fieldNum):
							for subfield in field:
								# append this subfield value to the correct field data in the record bucket
									if subfield[0] == 'c':
										fileData[fieldNum].append(subfield[1])
							
			for key in fileData.keys():
				if type(fileData[key]) is list:
					fileData[key] = '|'.join(fileData[key])
			output.append(fileData)
	print(json.dumps(output))


if __name__ == "__main__":
	main()
