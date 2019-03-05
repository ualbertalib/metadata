import time
from datetime import datetime
from fuzzywuzzy import fuzz
import urllib
import requests
import xml.etree.ElementTree as ETree
import json

#list of names
names = []
#populate name list from input file
with open('names.txt', 'r') as input:
    for line in input:
        names.append(line.replace('\n', ''))
    input.close()
    print (names)

log_file = "error.log"
query_type = "/authorities/names"
#APIs to be searched
apis = ['search_api_VF', 'search_api_VFP', 'search_api_VFC', 'search_api_LC', 'search_api_LCS']

def main():
    #save the results here
    results = "%s-%s%s" %("Results", datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S'), ".json")
    enriched_names = {}
    with open (results, 'w') as file:
        print ("total names = " + str(len(names)))
        for index, item in enumerate(names):
            print ("searching APIs for " + item + " " + str(index+1) + " of " + str(len(names)))
            enriched_names[item] = []
            for api in apis:
                # getting the API method
                name_result = APIFactory().get_API(item, query_type, api, log_file)
                # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                if name_result:
                    enriched_names[item].append(name_result)
        name_results = clean_up(enriched_names)
        result_names_Object = Results(name_results, names, file, 'name', log_file)
        final_names = result_names_Object.maximizer()

class APIFactory():
    @staticmethod
    def get_API(name, query_type, api, log_file):
        if api == 'search_api_LC':
            try:
                return SearchAPI(name, query_type, log_file).search_api_LC()
            except:
                PrintException(log_file, name)
        if api == 'search_api_LCS':
            try:
                return SearchAPI(name, query_type, log_file).search_api_LCS()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VF':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VF()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VFP':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VFP()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VFC':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VFC()
            except:
                PrintException(log_file, name)


class SearchAPI():
    def __init__(self, name , query_type, log_file):
        # this is needed for LC APIs only
        self.query_type = query_type
        # similarity function minimum cut-off score
        self.th = 95
        self.name = name
        # error reporting 
        self.log_file = log_file

    def search_api_VFP(self): 
        # dictionary for storing scores for this API
        self.scores = {}
        # The API call url
        viafP = "https://viaf.org/viaf/search?query=local.personalNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
        try:
            # decode the JSON
            viafP_result = requests.get(viafP).json()
            # if the are records in the result dict, iterate over them and get the VIAF_ID
            if 'records' in viafP_result['searchRetrieveResponse'].keys():
                for records in viafP_result['searchRetrieveResponse']['records']:
                    viaf_id = records['record']['recordData']['viafID']['#text']
                    # there might more than one data record (in form of a list). If so, iterate over them to get the "name"
                    if isinstance(records['record']['recordData']['mainHeadings']['data'], list):
                        for text in records['record']['recordData']['mainHeadings']['data']:
                            lcid = ''
                            # compare the "name" from the API to the name from the BIBFRAME. If the score is above the cut-off
                            # score then try and extract the coresponding LCID
                            candidateVP = text['text']
                            scoreVP = fuzz.token_sort_ratio(candidateVP, self.name)
                            if scoreVP > self.th:
                                if isinstance(text['sources']['sid'], list):
                                    for sid in text['sources']['sid']:
                                        if "LC" in sid:
                                            lcid = sid
                                else:
                                    if "LC" in text['sources']['sid']:
                                        lcid = text['sources']['sid']
                            if lcid != '':
                                # add the VIAF_ID, the "name" from VIAF and matching score (to be used later for stats reporting)
                                self.scores['VFP'] = {}
                                self.scores['VFP']['VIAFID'] = {}
                                self.scores['VFP']['VIAFID'][viaf_id] = [candidateVP, scoreVP]
                                # add the LCID
                                self.scores['VFP']['lcid'] = {}
                                self.scores['VFP']['lcid'][lcid] = []
                                self.scores['VFP']['lcid'][lcid].append(candidateVP)
                                self.scores['VFP']['lcid'][lcid].append(scoreVP)
                    else:
                        lcid = ''
                        candidateVP = records['record']['recordData']['mainHeadings']['data']['text']
                        scoreVP = fuzz.token_sort_ratio(candidateVP, self.name)
                        if scoreVP > self.th:
                            if isinstance(records['record']['recordData']['mainHeadings']['data']['sources']['sid'], list):
                                for sid in records['record']['recordData']['mainHeadings']['data']['sources']['sid']:
                                    if "LC" in sid:
                                        lcid = sid
                            else:
                                if "LC" in records['record']['recordData']['mainHeadings']['data']['sources']['sid']:
                                    lcid = records['record']['recordData']['mainHeadings']['data']['sources']['sid']
                            if lcid != '':
                                self.scores['VFP'] = {}
                                self.scores['VFP']['VIAFID'] = {}
                                self.scores['VFP']['VIAFID'][viaf_id] = [candidateVP, scoreVP]
                                self.scores['VFP']['lcid'] = {}
                                self.scores['VFP']['lcid'][lcid] = []
                                self.scores['VFP']['lcid'][lcid].append(candidateVP)
                                self.scores['VFP']['lcid'][lcid].append(scoreVP)
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return( (self.scores))

    def search_api_VFC(self):
        # dictionary for storing scores for this API
        self.scores = {}
        # The API call url
        viafC = "https://viaf.org/viaf/search?query=local.corporateNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
        try:
            # decode the JSON
            viafC_result = requests.get(viafC).json()
            # if the are records in the result dict, iterate over them and get the VIAF_ID
            if 'records' in viafC_result['searchRetrieveResponse'].keys():
                for recordsC in viafC_result['searchRetrieveResponse']['records']:
                    viaf_idC = recordsC['record']['recordData']['viafID']['#text']
                    # there might more than one data record (in form of a list). If so, iterate over them to get the "name"
                    if isinstance(recordsC['record']['recordData']['mainHeadings']['data'], list):
                        for textC in recordsC['record']['recordData']['mainHeadings']['data']:
                            lcidC = ''
                            # compare the "name" from the API to the name from the BIBFRAME. If the score is above the cut-off
                            # score then try and extract the coresponding LCID
                            candidateVC = textC['text']
                            scoreVC = fuzz.token_sort_ratio(candidateVC, self.name)
                            if scoreVC > self.th:
                                if isinstance(textC['sources']['sid'], list):
                                    for sidC in textC['sources']['sid']:
                                        if "LC" in sidC:
                                            lcidC = sidC
                                else:
                                    if "LC" in textC['sources']['sid']:
                                        lcidC = textC['sources']['sid']
                            if lcidC != '':
                                # add the VIAF_ID, the "name" from VIAF and matching score (to be used later for stats reporting)
                                self.scores['VFC'] = {}
                                self.scores['VFC']['VIAFID'] = {}
                                self.scores['VFC']['VIAFID'][viaf_idC] = [candidateVC, scoreVC]
                                # add the LCID
                                self.scores['VFC']['lcid'] = {}
                                self.scores['VFC']['lcid'][lcidC] = []
                                self.scores['VFC']['lcid'][lcidC].append(candidateVC)
                                self.scores['VFC']['lcid'][lcidC].append(scoreVC)
                    else:
                        lcidC = ''
                        candidateVC = recordsC['record']['recordData']['mainHeadings']['data']['text']
                        scoreVC = fuzz.token_sort_ratio(candidateVC, self.name)
                        if scoreVC > self.th:
                            if isinstance(recordsC['record']['recordData']['mainHeadings']['data']['sources']['sid'], list):
                                for sidC in recordsC['record']['recordData']['mainHeadings']['data']['sources']['sid']:
                                    if "LC" in sidC:
                                        lcidC = sidC
                            else:
                                if "LC" in recordsC['record']['recordData']['mainHeadings']['data']['sources']['sid']:
                                    lcidC = recordsC['record']['recordData']['mainHeadings']['data']['sources']['sid']
                            if lcidC != '':
                                self.scores['VFC'] = {}
                                self.scores['VFC']['VIAFID'] = {}
                                self.scores['VFC']['VIAFID'][viaf_idC] = [candidateVC, scoreVC]
                                self.scores['VFC']['lcid'] = {}
                                self.scores['VFC']['lcid'][lcidC] = []
                                self.scores['VFC']['lcid'][lcidC].append(candidateVC)
                                self.scores['VFC']['lcid'][lcidC].append(scoreVC)
        except:
            PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_api_VF(self):
        # dictionary for storing scores for this API
        self.scores = {}
        # The API call url
        viaf ="http://viaf.org/viaf/AutoSuggest?query=" + urllib.parse.quote(self.name.encode('utf8'))
        try:
            # decode the JSON
            viaf_result = requests.get(viaf).json()
            # if there is result in the dict, iterate over them and get the VIAF_ID and "name"
            if (viaf_result['result']):
                for item in viaf_result['result']:
                    candidateV = item['term']
                    vid = item['viafid']
                    scoreV = fuzz.token_sort_ratio(candidateV, self.name)
                    # if the similarity score is greater than the cut-off, add the VIAF_ID, "name" and similarity score to the dict
                    if scoreV > self.th:
                        self.scores['VFS'] = {}
                        self.scores['VFS']['VIAFID'] = {}
                        self.scores['VFS']['VIAFID'][vid] = [candidateV, scoreV]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_api_LCS(self):
        # dictionary for storing scores for this API
        self.scores = {}
        # The API call url
        suggest = "http://id.loc.gov" + self.query_type + '/suggest/?q=' + urllib.parse.quote(self.name.encode('utf8'))
        try:
            # decode the JSON
            suggest_result = requests.get(suggest).json()
            # iterate over all results
            for n in range(len(suggest_result[1])):
                # get hte "name"
                candidateS = suggest_result[1][n]
                # get the URI (LC ID)
                uriS = suggest_result[3][n].replace('http://id.loc.gov/authorities/names/', '')
                self.scoreSU = fuzz.token_sort_ratio(candidateS, self.name)
                # if the similarity socre is greater than the cut-off, add the "name" LC ID and similarity score to the dict
                if self.scoreSU > self.th:
                    self.scores['LCS'] = {}
                    self.scores['LCS']["lcid"] = {}
                    self.scores['LCS']["lcid"][uriS] = [candidateS, self.scoreSU]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_api_LC(self):
        # dictionary for storing scores for this API
        self.scores = {}
        # The API call url
        dym = "http://id.loc.gov" + self.query_type + "/didyoumean/?label=" + urllib.parse.quote(self.name.encode('utf8'))
        try:
            dym_result = requests.get(dym)
            # get the results in form of a XML tree 
            dym_results = ETree.fromstring(dym_result.content)
            for result in dym_results.iter('{http://id.loc.gov/ns/id_service#}term'):
                # get the "name"
                candidateD = result.text
                # get the URI (LC ID)
                uriD = result.get('uri')
                scoreD = fuzz.token_sort_ratio(candidateD, self.name)
                # if the similarity socre is greater than the cut-off, add the "name" LC ID and similarity score to the dict
                if scoreD > self.th:
                    self.scores['LC'] = {}
                    self.scores['LC']['lcid'] = {}
                    self.scores['LC']["lcid"][uriD] = [candidateD, scoreD]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

class Results():
    def __init__(self, results, source, file, type, log_file):
        # hold the dict for names and title when initiated
        self.results = results
        # hold the original naems or titles dict
        self.source = source
        self.file = file
        self.log_file = log_file
        self.final = {}
        self.type = type 

    def maximizer(self):
        # a dict for storing the maximum score for each API (only for VF and LC)
        self.maxs = {}
        try:
            # iterate over the results dict 
            for item in self.results.keys():
                scoreLC = []
                # adding temp values as a place holder for wmpty values
                # will be removed at the end of this process
                scoreLC.append("temp")
                scoreLC.append(0)
                scoreVF = []
                scoreVF.append("temp")
                scoreVF.append(0)
                # for each name find the URI with maximun score for VOAF and LC
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
                    # removing the temp place holders
                    if scoreLC[0] != "temp":
                        self.maxs[item]['LC'] = scoreLC
                    if scoreVF[0] != "temp":
                        self.maxs[item]['VIAF'] = scoreVF                  
        except:
            PrintException(self.log_file, name)
        json.dump(self.maxs, self.file)
        return(self.maxs)

def clean_up(l):
    for i in list(l):
        if l[i] == []:
            del l[i]
    return l

def PrintException(log_file, error):
    with open (log_file, "a+") as logs:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("\n")

if __name__ == "__main__":
    main()