import os
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
    file = "2015eresOrigbf.xml"
    apis = ['search_api_LC', 'search_api_LCS', 'search_api_VF', 'search_api_VFP', 'search_api_VFC']
    query_type = "/authorities/names"
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    bib_object = Bibframe(file)
    transformed = bib_object.convert_bibframe()
    names = bib_object.extract_names(transformed)
    print (str(len(names)) + " names were extracted")
    l = {}
    for index, item in enumerate(names.keys()):
        name = item.split('-_-_-')[0]
        print(index+1, name)
        l[item] = []
        for api in apis:
            result = APIFactory().get_API(name, query_type, api)
            if result:
                l[item].append(result)
    results = clean_up(l)
    result_Object = Results(results, names, file)
    result_Object.maximizer()
    f = result_Object.mapping()
    print (f)
    write(f, file)
    tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))

class Bibframe():
    def __init__(self, file):
        self.xslt = ET.parse("names_2.xsl")
        self.transform = ET.XSLT(self.xslt)
        self.doc = ET.parse(file)

    def convert_bibframe(self):
        self.transformed = self.transform(self.doc)
        return self.transformed

    def extract_names(self, transformed):
        self.names = {}
        self.transformed = transformed
        for i in str(self.transformed).split("\n"):
            if i != '':
                name = i.split("\t")[0]
                key = i.split("\t")[-1]
                type = i.split("\t")[1].replace('http://id.loc.gov/ontologies/bibframe/', '')
                checksum = name + "-_-_-" + type
                if checksum not in self.names.keys():
                    self.names[checksum] = []
                    self.names[checksum].append(key)
                else:
                    self.names[checksum].append(key)
        return self.names

class APIFactory():
    @staticmethod
    def get_API(name, query_type, api):
        if api == 'search_api_LC':
            return SearchAPI(name, query_type).search_api_LC()
        if api == 'search_api_LCS':
            return SearchAPI(name, query_type).search_api_LCS()
        if api == 'search_api_VF':
            return SearchAPI(name, query_type).search_api_VF()
        if api == 'search_api_VFP':
            return SearchAPI(name, query_type).search_api_VFP()
        if api == 'search_api_VFC':
            return SearchAPI(name, query_type).search_api_VFC()

class SearchAPI():
    def __init__(self, name , query_type):
        self.query_type = query_type
        self.th = 95
        self.name = name

    def search_api_VFP(self): 
        self.scores = {}
        viafP = "https://viaf.org/viaf/search?query=local.personalNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
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
        if len(self.scores) > 0:
            return( (self.scores))

    def search_api_VFC(self):
        self.scores = {}
        viafC = "https://viaf.org/viaf/search?query=local.corporateNames+all+%22" + urllib.parse.quote(self.name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
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
        if len(self.scores) > 0:
            return self.scores

    def search_api_VF(self):
        self.scores = {}
        viaf ="http://viaf.org/viaf/AutoSuggest?query=" + urllib.parse.quote(self.name.encode('utf8'))
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
        if len(self.scores) > 0:
            return self.scores

    def search_api_LCS(self):
        self.scores = {}
        suggest = "http://id.loc.gov" + self.query_type + '/suggest/?q=' + urllib.parse.quote(self.name.encode('utf8'))
        suggest_result = requests.get(suggest).json()
        for n in range(len(suggest_result[1])):
            candidateS = suggest_result[1][n]
            uriS = suggest_result[3][n].replace('http://id.loc.gov/authorities/names/', '')
            self.scoreSU = fuzz.token_sort_ratio(candidateS, self.name)
            if self.scoreSU > self.th:
                self.scores['LCS'] = {}
                self.scores['LCS']["lcid"] = {}
                self.scores['LCS']["lcid"][uriS] = [candidateS, self.scoreSU]
        if len(self.scores) > 0:
            return self.scores

    def search_api_LC(self):
        self.scores = {}
        dym = "http://id.loc.gov" + self.query_type + "/didyoumean/?label=" + urllib.parse.quote(self.name.encode('utf8'))
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
        if len(self.scores) > 0:
            return self.scores

class Results():
    def __init__(self, results, names, file):
        self.results = results
        self.names = names
        self.file = file
        self.final = {}

    def maximizer(self):
        self.maxs = {}
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
        return(self.maxs)
        
    def mapping(self):
        for i in self.maxs.keys():
            name = i.split('-_-_-')[0]
            type = i.split('-_-_-')[1]
            self.final[name] = {}
            self.final[name]['keys'] = []
            for keys in self.names[i]:
                self.final[name]['scores'] = self.maxs[i]
                self.final[name]['keys'].append(keys)
                
        print (len(self.final))
        return (self.final)

def write(final, file):
    enhanched = ETree.register_namespace('bf', 'http://id.loc.gov/ontologies/bibframe/')
    enhanched = ETree.register_namespace('bflc', 'http://id.loc.gov/ontologies/bflc/')
    enhanched = ETree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    enhanched = ETree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    enhanched = ETree.register_namespace('madsrdf', 'http://www.loc.gov/mads/rdf/v1#')
    enhanched = ETree.parse(file)
    with open('test.tsv', "w+") as output:
        output.write("ingest key" + "\t" + "viaf ID" + "\t" + "LC ID" + "\n") 
        for key in final.keys():
            try:
                LC = 'http://id.loc.gov/authorities/names/' + (final[key]['scores']['LC'][0])
                VF = 'http://viaf.org/viaf/' + (final[key]['scores']['VIAF'][0])
                for k in final[key]['keys']:
                    uri_key = k
                    output.write(uri_key + "\t" + VF + "\t" + LC + "\n")
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
    enhanched.write('output.xml')

def clean_up(l):
    for i in list(l):
        if l[i] == []:
            print (i)
            del l[i]
    return l

if __name__ == "__main__":
    main()