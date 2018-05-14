import os
import sys
import linecache
import statistics
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
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
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    folder = 'uploads'
    for files in os.listdir(folder):
        file = os.path.join(folder, files)
        filename = file.replace('.xml', '').replace('uploads/', '')
        print ("processing " + filename)
        log_file = filename.replace('.xml', '') + "-error-logs"
        output = filename.replace('.xml', '').replace("BIB/", "") + "-enhanced.xml" 
        clearLogs(log_file)
        apis = ['search_api_LC', 'search_api_LCS', 'search_api_VF', 'search_api_VFP', 'search_api_VFC']
        query_type = "/authorities/names"
        bib_object = Bibframe(file, log_file)
        transformed = bib_object.convert_bibframe()
        extracted = bib_object.extract_names(transformed)
        names = extracted[0]
        all_names = extracted[1]
        corp_names = extracted[2]
        print (str(all_names) + " were extrected from " + filename)
        print (str(len(names)) + " unique names were extracted from " + filename + " --- " + str(len(names) - corp_names) + " Personal names and " + str(corp_names) + " Corporate names")
        l = {}
        stats = {}
        for index, item in enumerate(names.keys()):
            name = item.split('-_-_-')[0]
            print(index+1, name)
            l[item] = []
            for api in apis:
                if api in stats.keys():
                    pass
                else:
                    stats[api] = 0
                result = APIFactory().get_API(name, query_type, api, log_file)
                if result:
                    l[item].append(result)
                    stats[api] = stats[api] + len(result)
        results = clean_up(l)
        result_Object = Results(results, names, file, log_file)
        result_Object.maximizer()
        f = result_Object.mapping()
        eff = get_stat(f, len(names), filename)
        stats['names-enriched'] = len(f)
        write(f, file, output, log_file, filename)
        tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        write_stats(eff, stats, filename, len(names), all_names, corp_names, datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
        tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))
    tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))

class Bibframe():
    def __init__(self, file, log_file):
        self.xslt = ET.parse("names_2.xsl")
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
        self.transformed = transformed
        try:
            count = 0
            corp_names = 0
            for i in str(self.transformed).split("\n"):
                if i != '':
                    count += 1
                    name = i.split("\t")[0]
                    key = i.split("\t")[-1]
                    type = i.split("\t")[1].replace('http://id.loc.gov/ontologies/bibframe/', '')
                    checksum = name + "-_-_-" + type
                    if checksum not in self.names.keys():
                        if type != 'Person':
                            corp_names += 1
                        self.names[checksum] = []
                        self.names[checksum].append(key)
                    else:
                        self.names[checksum].append(key)
        except:
            PrintException(self.log_file, name)
        return (self.names, count, corp_names)

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

class Results():
    def __init__(self, results, names, file, log_file):
        self.results = results
        self.names = names
        self.file = file
        self.log_file = log_file
        self.final = {}

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
        try:
            for i in self.maxs.keys():
                name = i.split('-_-_-')[0]
                type = i.split('-_-_-')[1]
                self.final[name] = {}
                self.final[name]['keys'] = []
                for keys in self.names[i]:
                    self.final[name]['scores'] = self.maxs[i]
                    self.final[name]['keys'].append(keys)
                    
            #print (len(self.final))
        except:
            PrintException(self.log_file, name)
        return (self.final)

def write(final, file, output, log_file, filename):
    clear_files(output)
    print ('writing ' + output)
    enhanched = ETree.register_namespace('bf', 'http://id.loc.gov/ontologies/bibframe/')
    enhanched = ETree.register_namespace('bflc', 'http://id.loc.gov/ontologies/bflc/')
    enhanched = ETree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    enhanched = ETree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    enhanched = ETree.register_namespace('madsrdf', 'http://www.loc.gov/mads/rdf/v1#')
    enhanched = ETree.parse(file)
    clear_TSV(filename)
    with open('TSVs/URIs-' + filename + '.tsv', "a") as tsv:
        tsv.write("name" + "\t" + "ingest key" + "\t" + "viaf ID" + "\t" + "LC ID" + "\n") 
        for key in final.keys():
            name = key.split('-_-_-')[0]
            LC = ''
            VF = ''
            try: 
                if "LC" in final[key]['scores']:
                    LC = 'http://id.loc.gov/authorities/names/' + (final[key]['scores']['LC'][0])
                if "VIAF" in final[key]['scores'].keys():
                    VF = 'http://viaf.org/viaf/' + (final[key]['scores']['VIAF'][0])
                for k in final[key]['keys']:
                    uri_key = k
                    tsv.write(name + "\t" + uri_key + "\t" + VF + "\t" + LC + "\n")
                    root = enhanched.getroot()
                    for element in root.iter('{http://id.loc.gov/ontologies/bibframe/}Agent'):
                        for ku in element.attrib.keys(): 
                            if element.attrib[ku] == uri_key:
                                if LC != '':
                                    element.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', LC)
                                if VF != '':
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

def clear_TSV(filename):
    folder = 'TSVs'
    file = 'URIs-' + filename + '.tsv'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def get_stat(f, names, file):
    folder = 'Diagrams'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
    stat = {}
    LC = 0
    VIAF = 0
    LC_Score = []
    VIAF_Score = []
    for i in f.keys():
        if "LC" in f[i]['scores'].keys():
            LC_Score.append(f[i]['scores']['LC'][1])
            LC += 1
        if "VIAF" in f[i]['scores'].keys():
            VIAF_Score.append(f[i]['scores']['VIAF'][1])
            VIAF += 1
    LC_Avg = statistics.mean(LC_Score)
    LC_Median = statistics.median(LC_Score)
    LC_Var = statistics.variance(LC_Score)
    LC_Std = statistics.stdev(LC_Score)
    VIAF_Avg = statistics.mean(VIAF_Score)
    VIAF_Median = statistics.median(VIAF_Score)
    VIAF_Var = statistics.variance(VIAF_Score)
    VIAF_Std = statistics.stdev(VIAF_Score)
    plt.hist(LC_Score, 10)
    plt.suptitle('Matching Score distribution for LC-IDs (' + file + ')', fontsize=12)
    plt.grid()
    plt.savefig(file_path+"-LC", facecolor='w', edgecolor='w',
        orientation='portrait')
    plt.clf()
    plt.hist(VIAF_Score, 10)
    plt.suptitle('Matching Score distribution for VIAF-IDs (' + file + ')', fontsize=12)
    plt.grid()
    plt.savefig(file_path+"-VIAF", facecolor='w', edgecolor='w',
        orientation='portrait')
    plt.clf()
    colors = ['red', 'green']
    labels = ['LC-IDs', 'VIAF-IDs']
    x_multi = [LC_Score, VIAF_Score]
    plt.hist(x_multi, 10, normed=1, histtype='bar', color=colors, label=labels)
    plt.legend(prop={'size': 10})
    plt.suptitle('Matching Score distribution (' + file + ')', fontsize=12)
    plt.savefig(file_path, facecolor='w', edgecolor='w',
        orientation='portrait')
    stat['LC'] = [LC, LC_Avg, LC_Median, LC_Var, LC_Std, (LC/names)*100]
    stat['VIAF'] = [VIAF, VIAF_Avg, VIAF_Median, VIAF_Var, VIAF_Std, (VIAF/names)*100]
    return (stat)

def write_stats(eff, stats, filename, names, all_names, corp_names, tf):
    file = filename + "-stats.tsv"
    if not os.path.exists("Stats"):
        os.makedirs("Stats")
    file_path = os.path.join("Stats", file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
    with open("Stats/" + file, "w+") as stat:
        stat.write(file + " was processed in " + str(tf) + "\n\n")
        stat.write(str(all_names) + " names were extracted from " +filename + "\n" + str(names) + " unique names " + " --- " + str(names - int(corp_names)) + " Personal names and " + str(corp_names) + " Corporate names" + "\n" + "\n")
        stat.write("API searched" +"\t" + "hits" + "\t" + "hit_rate" +"\n")
        for i in stats.keys():
            stat.write(i + "\t" + str(stats[i]) + "\t" + str((int(stats[i])/names)*100) + "\n")
        stat.write("\n" + "\n")
        stat.write('LC_ID' + '\n' + "names enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
        for i in eff["LC"]:
            stat.write(str(i) + "\t")
        stat.write("\n" + "\n")
        stat.write('VIAF_ID' + '\n' + "names enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
        for i in eff["VIAF"]:
            stat.write(str(i) + "\t")
        stat.write("\n" + "\n")

if __name__ == "__main__":
    main()