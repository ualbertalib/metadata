import lxml.etree as ET
from ..Utils import PrintException

class Bibframe():
    def __init__(self, file, log_file, merge):
        if merge == True:
            self.xslt = ET.parse("Webapp/Code/xslt/names_OCLC.xsl")
        else:
            self.xslt = ET.parse("Webapp/Code/xslt/names_OCLC_single.xsl")
        self.transform = ET.XSLT(self.xslt)
        self.doc = ET.parse(file)
        self.log_file = log_file

    def convert_bibframe(self):
        try: 
            dumy = ''
            self.transformed = self.transform(self.doc)
        except:
            PrintException(self.log_file, dumy)
        return self.transformed

    def extract_names(self, transformed):
        self.names = {}
        self.titles = {}
        self.transformed = transformed
        try:
            count = 0
            corp_names = 0
            for i in str(self.transformed).split("\n"):
                if i != '':
                    i = i.split("\t")
                    for ind, r in enumerate(i):
                        if r=='':
                            del i[ind]
                    if len(i) > 2:
                        title = i[0]
                        title_key = i[1]
                        if title not in self.titles.keys():
                            self.titles[title] = {}
                            self.titles[title]['keys'] = []
                            self.titles[title]['authors'] = []
                            self.titles[title]['keys'].append(title_key)
                        else:
                            self.titles[title]['keys'].append(title_key)
                        n = int((len(i)-2)/3)
                        for index in range(0, n):
                            count += 1
                            name = i[(index*3)+2]
                            key = i[(index*3)+4]
                            type = i[(index*3)+3].replace('http://id.loc.gov/ontologies/bibframe/', '')
                            checksum = name + "-_-_-" + type
                            if checksum not in self.names.keys():
                                if type != 'Person':
                                    corp_names += 1
                                self.names[checksum] = {}
                                self.names[checksum]["keys"] = []
                                self.names[checksum]['keys'].append(key)
                            else:
                                self.names[checksum]['keys'].append(key)
                            if checksum not in self.titles[title]['authors']:
                                self.titles[title]['authors'].append(checksum)
        except:
            PrintException(self.log_file, name)
        return (self.names, self.titles, count, corp_names)
