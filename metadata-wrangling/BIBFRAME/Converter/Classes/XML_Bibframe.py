import os
from os.path import isfile, join
import lxml.etree as ET

class XML_BIBFRAME():
    def __init__(self, master_file):
        self.folder = 'converted_BIBFRAME'
        self.master_file = master_file
        self.source = 'MARC_XML/%s' %(self.master_file)
        self.processing = 'Processing'
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if not os.path.exists(self.processing):
            os.makedirs(self.processing)
        self.subfolder = os.path.join(self.folder, self.master_file)
        if not os.path.exists(self.subfolder):
            os.makedirs(self.subfolder)
        self.xslt = ET.parse("marc2bibframe2-master/xsl/marc2bibframe2.xsl")
                
    def convert_to_BIBFRAME(self, number_of_records):
        for i, files in enumerate(os.listdir(self.source)):
            file = os.path.join(self.source, files)
            if os.path.isfile(file):
                output = os.path.join(self.subfolder, '')
                print ("Transforming record number %s of %s to BIBFRAME"  %(str(i+1), str(number_of_records)))
                dom = ET.parse(file)
                transform = ET.XSLT(self.xslt)
                newdom = transform(dom)
                with open (output + files, "w+") as BIBFRAME_file:
                    BIBFRAME_file.write(str(newdom).replace('<?xml version="1.0"?>', ''))
                    BIBFRAME_file.close()

    def merger(self):
        master_file = str(self.master_file) + '.xml'
        output = os.path.join(self.processing, master_file)
        with open(output, "w+") as merged_file:
            merged_file.write('<root>')
            for i, files in enumerate(os.listdir(self.subfolder)):
                file = os.path.join(self.subfolder, files)
                with open(file, 'r') as source:
                    for lines in source:
                        merged_file.write(lines)
                    source.close()
            merged_file.write('</root>')
            merged_file.close()