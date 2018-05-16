import os
import sys
import linecache
from time import sleep
from flask import Flask, request, redirect, url_for, send_from_directory, flash, render_template
from werkzeug.utils import secure_filename
from pymarc import MARCReader, XmlHandler, record_to_xml, XMLWriter
from os import listdir
import subprocess
from os.path import isfile, join
import lxml.etree as ET
import xml.etree.ElementTree as ETree
from fuzzywuzzy import fuzz
import urllib
import requests
import json
import time
from datetime import datetime

def main():
    file ='1985eresOrigbf.xml'
    print (file)
    #ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    log_file = file.replace('.xml', '') + "-error-logs"
    output = file.replace('.xml', '').replace("BIB/", "") + "-enhanced-test.xml" 
    clearLogs(log_file)
    apis = ['search_api_LC', 'search_api_LCS', 'search_api_VF', 'search_api_VFP', 'search_api_VFC']
    query_type = "/authorities/names"
    bib_object = Bibframe(file, log_file)
    transformed = bib_object.convert_bibframe()
    names = bib_object.extract_names(transformed)[0]
    titles = bib_object.extract_names(transformed)[1]
    print (titles)
    print (str(len(names)) + " names were extracted from " + file)
    print (str(len(titles)) + " titles were extracted from " + file)
    enriched_names = {}
    enriched_titles = {}
    print ("enriching names")
    for index, item in enumerate(names.keys()):
        name = item.split('-_-_-')[0]
        print(index+1, name)
        enriched_names[item] = []
        for api in apis:
            name_result = APIFactory().get_API(name, query_type, api, log_file)
            if name_result:
                enriched_names[item].append(name_result)
    print ("enriching titles")
    for index, title in enumerate(titles.keys()):
        print(index+1, title)
        for authors in titles[title]['authors']:
            author =  authors.split('-_-_-')[0]
            key = str(author) + "-_-_-" + str(title)
            enriched_titles[key] = []
            title_result = APIFactory().get_API(author, title, 'search_OCLC', log_file)
            #print (title_result)
            if title_result:
                enriched_titles[key].append(title_result)
    name_results = clean_up(enriched_names)
    title_result = clean_up(enriched_titles)
    #print (name_result)
    #print (title_result)
    result_names_Object = Results(name_results, names, file, 'name', log_file)
    result_names_Object.maximizer()
    final_names = result_names_Object.mapping()
    result_title_Object = Results(title_result, titles, file, 'title', log_file)
    final_title = result_title_Object.mapping()
    write(final_names, final_title, file, output, log_file)
    #tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    #print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))

class Bibframe():
    def __init__(self, file, log_file):
        self.xslt = ET.parse("names_OCLC.xsl")
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
                            name = i[(index*3)+2]
                            key = i[(index*3)+4]
                            type = i[(index*3)+3].replace('http://id.loc.gov/ontologies/bibframe/', '')
                            checksum = name + "-_-_-" + type
                            if checksum not in self.names.keys():
                                self.names[checksum] = {}
                                self.names[checksum]["keys"] = []
                                self.names[checksum]['keys'].append(key)
                            else:
                                self.names[checksum]['keys'].append(key)
                            if checksum not in self.titles[title]['authors']:
                                self.titles[title]['authors'].append(checksum)
        except:
            PrintException(self.log_file, name)
        return (self.names, self.titles)

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
        if api == 'search_OCLC':
            try:
                return SearchAPI(name, query_type, log_file).search_OCLC()
            except:
                PrintException(log_file, name)

class SearchAPI():
    def __init__(self, name , query_type, log_file):
        self.query_type = query_type
        self.th = 95
        self.name = name
        self.log_file = log_file

    def search_api_VFP(self): 
        self.scores = {}
        viafP = "https://viaf.org/viaf/search?query=local.personalNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
        try:
            viafP_result = requests.get(viafP).json()
            if 'records' in viafP_result['searchRetrieveResponse'].keys():
                for records in viafP_result['searchRetrieveResponse']['records']:
                    viaf_id = records['record']['recordData']['viafID']['#text']
                    if isinstance(records['record']['recordData']['v:mainHeadings']['data'], list):
                        for text in records['record']['recordData']['v:mainHeadings']['data']:
                            lcid = ''
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
                                self.scores['VFP'] = {}
                                self.scores['VFP']['VIAFID'] = {}
                                self.scores['VFP']['VIAFID'][viaf_id] = [candidateVP, scoreVP]
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
        self.scores = {}
        viafC = "https://viaf.org/viaf/search?query=local.corporateNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
        try:
            viafC_result = requests.get(viafC).json()
            if 'records' in viafC_result['searchRetrieveResponse'].keys():
                for recordsC in viafC_result['searchRetrieveResponse']['records']:
                    viaf_idC = recordsC['record']['recordData']['viafID']['#text']
                    if isinstance(recordsC['record']['recordData']['v:mainHeadings']['data'], list):
                        for textC in recordsC['record']['recordData']['v:mainHeadings']['data']:
                            lcidC = ''
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
                                self.scores['VFC'] = {}
                                self.scores['VFC']['VIAFID'] = {}
                                self.scores['VFC']['VIAFID'][viaf_idC] = [candidateVC, scoreVC]
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
        self.scores = {}
        viaf ="http://viaf.org/viaf/AutoSuggest?query=" + urllib.parse.quote(self.name.encode('utf8'))
        try:
            viaf_result = requests.get(viaf).json()
            if (viaf_result['result']):
                for item in viaf_result['result']:
                    candidateV = item['term']
                    vid = item['viafid']
                    scoreV = fuzz.token_sort_ratio(candidateV, self.name)
                    if scoreV > self.th:
                        self.scores['VFS'] = {}
                        self.scores['VFS']['VIAFID'] = {}
                        self.scores['VFS']['VIAFID'][vid] = [candidateV, scoreV]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_api_LCS(self):
        self.scores = {}
        suggest = "http://id.loc.gov" + self.query_type + '/suggest/?q=' + urllib.parse.quote(self.name.encode('utf8'))
        try:
            suggest_result = requests.get(suggest).json()
            for n in range(len(suggest_result[1])):
                candidateS = suggest_result[1][n]
                uriS = suggest_result[3][n].replace('http://id.loc.gov/authorities/names/', '')
                self.scoreSU = fuzz.token_sort_ratio(candidateS, self.name)
                if self.scoreSU > self.th:
                    self.scores['LCS'] = {}
                    self.scores['LCS']["lcid"] = {}
                    self.scores['LCS']["lcid"][uriS] = [candidateS, self.scoreSU]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_api_LC(self):
        self.scores = {}
        dym = "http://id.loc.gov" + self.query_type + "/didyoumean/?label=" + urllib.parse.quote(self.name.encode('utf8'))
        try:
            dym_result = requests.get(dym)
            dym_results = ETree.fromstring(dym_result.content)
            for result in dym_results.iter('{http://id.loc.gov/ns/id_service#}term'):
                candidateD = result.text
                uriD = result.get('uri')
                scoreD = fuzz.token_sort_ratio(candidateD, self.name)
                if scoreD > self.th:
                    self.scores['LC'] = {}
                    self.scores['LC']['lcid'] = {}
                    self.scores['LC']["lcid"][uriD] = [candidateD, scoreD]
        except:
                PrintException(self.log_file, self.name)
        if len(self.scores) > 0:
            return self.scores

    def search_OCLC(self):
        self.scores = {}
        OCLC = "http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q=" + self.query_type + "&wskey=1QSLAhHnqyQYTlcnREquxaYmTBEng0FbYgPUwa5clqNAmG1Qe8m0LsqRxh22iTfoi1TGdOMloHfTjzXf"
        try:
            OCLC_result = requests.get(OCLC).text
            with open("temp-file.xml", "w") as file:
                file.write(OCLC_result)
                file.close()
            file = ETree.parse("temp-file.xml")
            root = file.getroot()
            for i in root.iter('{http://www.w3.org/2005/Atom}entry'):
                author = i.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
                title = i.find('{http://www.w3.org/2005/Atom}title').text
                id = i.find('{http://www.w3.org/2005/Atom}id').text
                scoreTitle = fuzz.token_sort_ratio(title, self.query_type)
                if scoreTitle > self.th:
                    scoreOCLC = fuzz.token_sort_ratio(author, self.name)
                    if scoreOCLC > self.th:
                        score = (scoreTitle + scoreOCLC)/2
                        work_id = ''
                        wid = id.replace('http://worldcat.org/oclc/', '')
                        self.scores['OCLC'] = {}
                        self.scores['OCLC']['oclcid'] = {}
                        self.scores['OCLC']['oclcid'][wid] = [self.query_type, scoreTitle]
                        workid = 'http://experiment.worldcat.org/oclc/' + wid + '.jsonld'
                        OCLC_res = requests.get(workid).json()
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
                    self.final[title] = {}
                    self.final[title]['keys'] = []
                    for keys in self.source[title]['keys']:
                        self.final[title]['scores'] = self.results[i]
                        self.final[title]['keys'].append(keys)
            except:
                PrintException(self.log_file, name)
            print (self.final)
            return (self.final)

def write(final, file, output, log_file):
    clear_files(output)
    print ('writing ' + output)
    enhanched = ETree.register_namespace('bf', 'http://id.loc.gov/ontologies/bibframe/')
    enhanched = ETree.register_namespace('bflc', 'http://id.loc.gov/ontologies/bflc/')
    enhanched = ETree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    enhanched = ETree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    enhanched = ETree.register_namespace('madsrdf', 'http://www.loc.gov/mads/rdf/v1#')
    enhanched = ETree.parse(file)
    with open('URIs.tsv', "a") as tsv:
        tsv.write("ingest key" + "\t" + "viaf ID" + "\t" + "LC ID" + "\n") 
        for key in final.keys():
            name = key.split('-_-_-')[0]
            try:
                if "LC" in final[key]['scores']:
                    LC = 'http://id.loc.gov/authorities/names/' + (final[key]['scores']['LC'][0])
                if "VIAF" in final[key]['scores'].keys():
                    VF = 'http://viaf.org/viaf/' + (final[key]['scores']['VIAF'][0])
                for k in final[key]['keys']:
                    uri_key = k
                    tsv.write(uri_key + "\t" + VF + "\t" + LC + "\n")
                    root = enhanched.getroot()
                    for element in root.iter('{http://id.loc.gov/ontologies/bibframe/}Agent'):
                        for ku in element.attrib.keys(): 
                            if element.attrib[ku] == uri_key:
                                element.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', LC)
                                a = ETree.SubElement(element, 'bf:identifiedBy')
                                b = ETree.SubElement(a, 'bf:IdentifiedBy')
                                c = ETree.SubElement(b, 'rdf:value')
                                c.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', VF)
            except:
                print ("could not find identfier for " + key)
                PrintException(log_file, name)
    enhanched.write("enhanced-files/" + output)

def clean_up(l):
    for i in list(l):
        if l[i] == []:
            print (i)
            del l[i]
    return l

def PrintException(log_file, error):
    with open ("logs/" + log_file, 'a') as logs:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("EXCEPTION IN (%s, LINE %s '%s'): %s name: %s" % (filename, lineno, line.strip(), exc_obj, error))
        logs.write("\n")

def clearLogs(log_file):
    folder = 'logs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, log_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def clear_files(output):
    folder = 'enhanced-files'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, output)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
