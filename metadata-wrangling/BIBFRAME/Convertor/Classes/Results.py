from Utils import PrintException

class Results():
    def __init__(self, results, source, file, type, log_file):
        self.results = results
        self.source = source
        self.file = file
        self.log_file = log_file
        self.final = {}
        self.type = type 

    def maximizer(self):
        self.maxs = {}
        try:
            for item in self.results.keys():
                name = item.split('-_-_-')[0]
                scoreLC = []
                scoreLC.append("temp")
                scoreLC.append(0)
                scoreVF = []
                scoreVF.append("temp")
                scoreVF.append(0)
                for itr in self.results[item]:
                    for it in itr.keys():
                        if 'lcid' in itr[it].keys():
                            for k in itr[it]['lcid'].keys():
                                if itr[it]['lcid'][k][-1] > scoreLC[-1]:
                                    scoreLC[0] = k.replace('LC|', '').replace(' ', '')
                                    scoreLC[1] = itr[it]['lcid'][k][-1]
                        if 'VIAFID' in itr[it].keys():
                            for k in itr[it]['VIAFID'].keys():
                                if itr[it]['VIAFID'][k][-1] > scoreVF[-1]:
                                    scoreVF[0] = k
                                    scoreVF[1] = itr[it]['VIAFID'][k][-1]
                if scoreVF[0] != "temp" or scoreLC[0] != "temp":                   
                    self.maxs[item] = {} 
                    if scoreLC[0] != "temp":
                        self.maxs[item]['LC'] = scoreLC
                    if scoreVF[0] != "temp":
                        self.maxs[item]['VIAF'] = scoreVF                  
        except:
            PrintException(self.log_file, name)
        return(self.maxs)
        
    def mapping(self):
        if self.type == 'name':
            try:
                for i in self.maxs.keys():
                    name = i.split('-_-_-')[0]
                    type = i.split('-_-_-')[1]
                    self.final[name] = {}
                    self.final[name]['keys'] = []
                    for keys in self.source[i]['keys']:
                        self.final[name]['scores'] = self.maxs[i]
                        self.final[name]['keys'].append(keys)
            except:
                PrintException(self.log_file, name)
            return (self.final)
        elif self.type == 'title':
            try:
                for i in self.results.keys():
                    title = i.split('-_-_-')[1]
                    if 'oclcid' in self.results[i][0]['OCLC'].keys():
                        oclcid = []
                        for id in self.results[i][0]['OCLC']['oclcid'].keys():
                            oclcid.append('http://worldcat.org/oclc/' + id)
                            oclcid.append(self.results[i][0]['OCLC']['oclcid'][id][1])
                    if 'work_id' in self.results[i][0]['OCLC'].keys():
                        work_id = []
                        for id in self.results[i][0]['OCLC']['work_id'].keys():
                            work_id.append(id)
                            work_id.append(self.results[i][0]['OCLC']['work_id'][id][1])
                    if len(oclcid) > 0 or len(work_id) > 0:
                        ID = {}
                        if len(oclcid) > 0:
                            ID['oclcid'] = oclcid
                        if len(work_id) > 0:
                            ID['work_id'] = work_id
                        self.final[title] = {}
                        self.final[title]['keys'] = []
                        for keys in self.source[title]['keys']:
                            self.final[title]['scores'] = ID
                            self.final[title]['keys'].append(keys)
            except:
                PrintException(self.log_file, name)
            return (self.final)