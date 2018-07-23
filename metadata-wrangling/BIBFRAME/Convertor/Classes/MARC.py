import os
from os.path import isfile, join
from pymarc import MARCReader, XmlHandler, record_to_xml, XMLWriter
from Classes.XML_Bibframe import XML_BIBFRAME
import time
from datetime import datetime

class MARC_XML():
    def __init__(self):
        self.source = 'marc'
        self.folder = 'MARC_XML'
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def convert_marc_xml(self):
        for index, files in enumerate(os.listdir(self.source)):
            subfolder_name = '%s_%s' %(files.split('.')[0], datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            sufolder = os.path.join(self.folder, subfolder_name)
            if not os.path.exists(sufolder):
                os.makedirs(sufolder)
            #create the BIBFRAME converter object
            BIBFRAME = XML_BIBFRAME(subfolder_name)
            file = os.path.join(self.source, files)
            output = os.path.join(sufolder, '')
            with open(file, "rb") as marc_file:
                reader = MARCReader(marc_file, to_unicode=True, force_utf8=False, utf8_handling='ignore')
                for i, record in enumerate(reader):
                    print ("converting record number %s of file number %s to XML" %(str(i), str(index+1)))
                    if record.title():
                        ti = record.title()
                        ti = ti.replace("/", "")
                        ti = ti.replace(" ", "_")
                        ti = ti[0:50]
                        writer = XMLWriter(open(output + ti + '.xml','wb'))
                        writer.write(record)
                        writer.close()
                    else:
                        writer = XMLWriter(open(output + 'unknownTitle' + str(i) + '.xml','wb'))
                marc_file.close()
            #convert MARC/XML to BIBFRAME
            BIBFRAME.convert_to_BIBFRAME(i)
            BIBFRAME.merger()