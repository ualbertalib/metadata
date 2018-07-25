from Utils import PrintException
from fuzzywuzzy import fuzz
import urllib
import requests
# change this to import your personal OCLC wskey
from Passwords import keys
import xml.etree.ElementTree as ETree
import json

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
                    if isinstance(records['record']['recordData']['v:mainHeadings']['data'], list):
                        for text in records['record']['recordData']['v:mainHeadings']['data']:
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
                        candidateVP = records['record']['recordData']['v:mainHeadings']['data']['text']
                        scoreVP = fuzz.token_sort_ratio(candidateVP, self.name)
                        if scoreVP > self.th:
                            if isinstance(records['record']['recordData']['v:mainHeadings']['data']['sources']['sid'], list):
                                for sid in records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                                    if "LC" in sid:
                                        lcid = sid
                            else:
                                if "LC" in records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                                    lcid = records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']
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
                    if isinstance(recordsC['record']['recordData']['v:mainHeadings']['data'], list):
                        for textC in recordsC['record']['recordData']['v:mainHeadings']['data']:
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
                        candidateVC = recordsC['record']['recordData']['v:mainHeadings']['data']['text']
                        scoreVC = fuzz.token_sort_ratio(candidateVC, self.name)
                        if scoreVC > self.th:
                            if isinstance(recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid'], list):
                                for sidC in recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                                    if "LC" in sidC:
                                        lcidC = sidC
                            else:
                                if "LC" in recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                                    lcidC = recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']
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

    def search_OCLC(self):
        # since this API does not need a query_type, this variable was used to pass the title to the object
        # dictionary for storing scores for this API
        self.scores = {}
        #import your OCLC develpoer key
        wskey = keys['OCLC-wskey'][0]
        # The API call url
        OCLC = "http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q=" + self.query_type + "&wskey=%s" %(wskey)
        try:
            OCLC_result = requests.get(OCLC).text
            # having issues reading the response object. Work around: Write to a file and then read -- the file will be deleted at the end of the process
            with open("temp-file.xml", "w") as file:
                file.write(OCLC_result)
                file.close()
            file = ETree.parse("temp-file.xml")
            root = file.getroot()
            # iterate over the root element and get "title", "author" (name), and "id" (worldcat ID) for each entry 
            for i in root.iter('{http://www.w3.org/2005/Atom}entry'):
                author = i.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
                title = i.find('{http://www.w3.org/2005/Atom}title').text
                id = i.find('{http://www.w3.org/2005/Atom}id').text
                # if title was a match (>%95) and author was a match also, then start the process for getting the work_id
                scoreTitle = fuzz.token_sort_ratio(title, self.query_type)
                if scoreTitle > self.th:
                    scoreOCLC = fuzz.token_sort_ratio(author, self.name)
                    if scoreOCLC > self.th:
                        # use this score as the average score
                        score = (scoreTitle + scoreOCLC)/2
                        work_id = ''
                        # get the worldcat ID
                        wid = id.replace('http://worldcat.org/oclc/', '')
                        # store the worldcat ID in the dict -- this ID is not used for enrichment at this point
                        self.scores['OCLC'] = {}
                        self.scores['OCLC']['oclcid'] = {}
                        self.scores['OCLC']['oclcid'][wid] = [self.query_type, scoreTitle]
                        # create the query url and send it to worldcat to get back the JSON-LD
                        workid = 'http://experiment.worldcat.org/oclc/' + wid + '.jsonld'
                        # decode the JSON
                        OCLC_res = requests.get(workid).json()
                        # iterate over the JSON graph and find work_id
                        for i in OCLC_res['@graph']:
                            if 'exampleOfWork' in i.keys():
                                work_id = i['exampleOfWork']
                        if work_id != '':
                            self.scores['OCLC']['work_id'] = {}
                            self.scores['OCLC']['work_id'][work_id] = [self.query_type, score]
        except:
            PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return (self.scores)