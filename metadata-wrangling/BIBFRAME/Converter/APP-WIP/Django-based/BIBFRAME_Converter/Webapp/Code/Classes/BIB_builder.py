import os
import time
from os.path import isfile, join
from datetime import datetime

class BIB_builder():
    def __init__(self):
        # folder to store BIBFRAME files
        self.source = 'Webapp/Files/Processing/BIBFRAME'
        if not os.path.exists(self.source):
            os.makedirs(self.source)
        # processing folder
        self.folder = 'Webapp/Files/Processing'
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def merger(self):
        f_name = ''
        output = '%s/Merged-file_%s.xml' %(self.folder, datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        with open(output, "w+") as merged_file:
                merged_file.write('<root>')
                # for all files in the BIBFRAME folder
                for files in [files for files in os.listdir(self.source) if isfile(join(self.source, files))]:
                    # check if it is a marc file
                    if files.endswith('.xml'):
                        f_name = f_name + '--__--__--' + str(files)
                        file = join(self.source, files)
                        with open(file, 'r') as source_file:
                            for lines in source_file:
                                merged_file.write(lines)
                            source_file.close()
                merged_file.write('</root>')
                merged_file.close()
        return (output, f_name)