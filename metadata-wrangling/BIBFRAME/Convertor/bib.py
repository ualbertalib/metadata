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


#subprocess.call(['java', '-jar', 'saxon9he.jar', '-t' '-s:1985eresOrigbf.xml -xsl:names_2.xsl -o:test.tsv'])
#subprocess.call(["saxon9he.jar", "-o:output.xml", "-s:file.xml", "file.xslt"])

#with open("1985eresOrigbf.xml", "rb") as f:
xslt = ET.parse("names_2.xsl")
dom = ET.parse("1985eresOrigbf.xml")
    #r = dom.xpath('//bf:Agent[@rdf:about]/@rdf:about', namespaces={'bf': 'http://id.loc.gov/ontologies/bibframe/', 'rdf' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
    #root = dom.getroot()
    #for neighbor in root.iter('{http://id.loc.gov/ontologies/bibframe/}Agent'):
     #   if "{'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about': 'http://example.org/3825414#Agent100-16'}" in neighbor.attrib:
      #      print (neighbor.attrib)
transform = ET.XSLT(xslt)
newdom = transform(dom)
l = {}
th = 95
query_type = "/authorities/names"
names = {}
for i in str(newdom).split("\n"):
    if i != '':
        name = i.split("\t")[0]
        key = i.split("\t")[-1]
        type = i.split("\t")[1]
        checksum = name + "-_-_-" + type
        if checksum not in names.keys():
            names[checksum] = []
            names[checksum].append(key)
        else:
            names[checksum].append(key)
for n, i in enumerate(names.keys()):
    name = i.split('-_-_-')[0]
    print (name, n) 
    scores = {}
    viafP = "https://viaf.org/viaf/search?query=local.personalNames+all+%22" + urllib.parse.quote(name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
    viafC = "https://viaf.org/viaf/search?query=local.corporateNames+all+%22" + urllib.parse.quote(name.encode('utf8')) + "%22&sortKeys=holdingscount&recordSchema=BriefVIAF&httpAccept=application/json"
    viaf ="http://viaf.org/viaf/AutoSuggest?query=" + urllib.parse.quote(name.encode('utf8'))
    suggest = "http://id.loc.gov" + query_type + '/suggest/?q=' + urllib.parse.quote(name.encode('utf8'))
    dym = "http://id.loc.gov" + query_type + "/didyoumean/?label=" + urllib.parse.quote(name.encode('utf8'))
    viaf_result = requests.get(viaf).json()
    viafP_result = requests.get(viafP).json()
    viafC_result = requests.get(viafC).json()
    suggest_result = requests.get(suggest).json()
    dym_result = requests.get(dym)
    dym_results = ETree.fromstring(dym_result.content)
    if 'records' in viafP_result['searchRetrieveResponse'].keys():
        for records in viafP_result['searchRetrieveResponse']['records']:
            viaf_id = records['record']['recordData']['viafID']['#text']
            if isinstance(records['record']['recordData']['v:mainHeadings']['data'], list):
                for text in records['record']['recordData']['v:mainHeadings']['data']:
                    lcid = ''
                    candidateVP = text['text']
                    scoreVP = fuzz.token_sort_ratio(candidateVP, name)
                    if scoreVP > th:
                        if isinstance(text['sources']['sid'], list):
                            for sid in text['sources']['sid']:
                                if "LC" in sid:
                                    lcid = sid
                        else:
                            if "LC" in text['sources']['sid']:
                                lcid = text['sources']['sid']
                    if lcid != '':
                        scores['VFP'] = {}
                        scores['VFP']['VIAFID'] = {}
                        scores['VFP']['VIAFID'][viaf_id] = [candidateVP, scoreVP]
                        scores['VFP']['lcid'] = {}
                        scores['VFP']['lcid'][lcid] = []
                        scores['VFP']['lcid'][lcid].append(candidateVP)
                        scores['VFP']['lcid'][lcid].append(scoreVP)
            else:
                lcid = ''
                candidateVP = records['record']['recordData']['v:mainHeadings']['data']['text']
                scoreVP = fuzz.token_sort_ratio(candidateVP, name)
                if scoreVP > th:
                    if isinstance(records['record']['recordData']['v:mainHeadings']['data']['sources']['sid'], list):
                        for sid in records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                            if "LC" in sid:
                                lcid = sid
                    else:
                        if "LC" in records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                            lcid = records['record']['recordData']['v:mainHeadings']['data']['sources']['sid']
                    if lcid != '':
                        scores['VFP'] = {}
                        scores['VFP']['VIAFID'] = {}
                        scores['VFP']['VIAFID'][viaf_id] = [candidateVP, scoreVP]
                        scores['VFP']['lcid'] = {}
                        scores['VFP']['lcid'][lcid] = []
                        scores['VFP']['lcid'][lcid].append(candidateVP)
                        scores['VFP']['lcid'][lcid].append(scoreVP)
    if 'records' in viafC_result['searchRetrieveResponse'].keys():
        for recordsC in viafC_result['searchRetrieveResponse']['records']:
            viaf_idC = recordsC['record']['recordData']['viafID']['#text']
            if isinstance(recordsC['record']['recordData']['v:mainHeadings']['data'], list):
                for textC in recordsC['record']['recordData']['v:mainHeadings']['data']:
                    lcidC = ''
                    candidateVC = textC['text']
                    scoreVC = fuzz.token_sort_ratio(candidateVC, name)
                    if scoreVC > th:
                        if isinstance(textC['sources']['sid'], list):
                            for sidC in textC['sources']['sid']:
                                if "LC" in sidC:
                                    lcidC = sidC
                        else:
                            if "LC" in textC['sources']['sid']:
                                lcidC = textC['sources']['sid']
                    if lcidC != '':
                        scores['VFC'] = {}
                        scores['VFC']['VIAFID'] = {}
                        scores['VFC']['VIAFID'][viaf_idC] = [candidateVC, scoreVC]
                        scores['VFC']['lcid'] = {}
                        scores['VFC']['lcid'][lcidC] = []
                        scores['VFC']['lcid'][lcidC].append(candidateVC)
                        scores['VFC']['lcid'][lcidC].append(scoreVC)
            else:
                lcidC = ''
                candidateVC = recordsC['record']['recordData']['v:mainHeadings']['data']['text']
                scoreVC = fuzz.token_sort_ratio(candidateVC, name)
                if scoreVC > th:
                    if isinstance(recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid'], list):
                        for sidC in recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                            if "LC" in sidC:
                                lcidC = sidC
                    else:
                        if "LC" in recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']:
                            lcidC = recordsC['record']['recordData']['v:mainHeadings']['data']['sources']['sid']
                    if lcidC != '':
                        scores['VFC'] = {}
                        scores['VFC']['VIAFID'] = {}
                        scores['VFC']['VIAFID'][viaf_idC] = [candidateVC, scoreVC]
                        scores['VFC']['lcid'] = {}
                        scores['VFC']['lcid'][lcidC] = []
                        scores['VFC']['lcid'][lcidC].append(candidateVC)
                        scores['VFC']['lcid'][lcidC].append(scoreVC)
    if (viaf_result['result']):
        for item in viaf_result['result']:
            candidateV = item['term']
            vid = item['viafid']
            scoreV = fuzz.token_sort_ratio(candidateV, name)
            if scoreV > th:
                scores['VFS'] = {}
                scores['VFS']['VIAFID'] = {}
                scores['VFS']['VIAFID'][vid] = [candidateV, scoreV]
    for n in range(len(suggest_result[1])):
        candidateS = suggest_result[1][n]
        uriS = suggest_result[3][n].replace('http://id.loc.gov/authorities/names/', '')
        scoreS = fuzz.token_sort_ratio(candidateS, name)
        if scoreS > th:
            scores['LCS'] = {}
            scores['LCS']["lcid"] = {}
            scores['LCS']["lcid"][uriS] = [candidateS, scoreS]
    for result in dym_results.iter('{http://id.loc.gov/ns/id_service#}term'):
        candidateD = result.text
        uriD = result.get('uri')
        scoreD = fuzz.token_sort_ratio(n, name)
        if scoreD > th:
            scores['LC'] = {}
            scores['LC']['lcid'] = {}
            scores['LC']["lcid"][uriS] = [candidateD, scoreS]
    if len(scores) > 0:
        #l[i] = []
        #l[i].append(i.split("\t")[0])
        #l[key].append(i.split("\t")[1].replace('http://id.loc.gov/ontologies/bibframe/', ''))
        l[i] = scores

#print (l)
final = {}
for item in l.keys():
    name = item.split('-_-_-')[0]
    scoreLC = []
    scoreLC.append("temp")
    scoreLC.append(0)
    scoreVF = []
    scoreVF.append("temp")
    scoreVF.append(0)
    for itr in l[item].keys():
        if 'lcid' in l[item][itr].keys():
            for k in l[item][itr]['lcid'].keys():
                if l[item][itr]['lcid'][k][-1] > scoreLC[-1]:
                    scoreLC[0] = k
                    scoreLC[1] = l[item][itr]['lcid'][k][-1]
        if 'VIAFID' in l[item][itr].keys():
            for k in l[item][itr]['VIAFID'].keys():
                if l[item][itr]['VIAFID'][k][-1] > scoreVF[-1]:
                    scoreVF[0] = k
                    scoreVF[1] = l[item][itr]['VIAFID'][k][-1]
                        
    final[name] = {}
    final[name]['LC'] = scoreLC
    final[name]['VIAF'] = scoreVF
print (len(l))
print (final)
print (len(final))



'''with open ("test-result.tsv", "r") as oo:
 #   oo.write(str(newdom).replace('<?xml version="1.0"?>', ''))
    for i in oo:
        print (i)'''

'''if __name__ == '__main__':
    from optparse import OptionParser

    oparser = OptionParser()
    oparser.add_option('-d', '--debug', action='store_true', default=False)
    opts, args = oparser.parse_args()
    app.debug = opts.debug
    app.run(host='0.0.0.0')'''
