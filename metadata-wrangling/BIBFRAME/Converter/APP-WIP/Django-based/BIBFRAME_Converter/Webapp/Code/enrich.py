import os
import statistics
from .Classes.MARC import MARC_XML
from .Classes.Bibframe import Bibframe
from .Classes.APIFactory import APIFactory
from .Classes.Results import Results
from .Classes.BIB_builder import BIB_builder
from .Utils import clean_up, PrintException, clearLogs, clear_files, clear_TSV, delete_temp, clear_processing
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ETree
import time
from datetime import datetime

def main(file):
    #proccess start time
    tps = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')    
    # delete files in the processing folder
    clear_processing()
    #convert .mrc to MARC/XML
    Marc_XML = MARC_XML(file)
    Marc_XML.convert_marc_xml()
    #BIBFRAME = BIB_builder()
    #BIBFRAME.merger()
    folder = 'Webapp/Processing'
    #iterate over BIBFRAME files
    for files in os.listdir(folder):
        tfs = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        file = os.path.join(folder, files)
        filename = files.replace('.xml', '')
        print ("processing " + filename)
        ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        log_file = str(filename) + "-error-logs"
        output = str(filename) + "-enhanced.xml" 
        clearLogs(log_file, filename)
        # all the APIs that will be searched - for a new API, add a new method to SearchAPI class and call it with adding a staticmethod to APIFactory
        apis = ['search_api_LC', 'search_api_LCS', 'search_api_VF', 'search_api_VFP', 'search_api_VFC']
        #this is needed for LC APIs
        query_type = "/authorities/names"
        # extracting names and titles from BIBFRAME
        bib_object = Bibframe(file, log_file)
        transformed = bib_object.convert_bibframe()
        names = bib_object.extract_names(transformed)[0]
        titles = bib_object.extract_names(transformed)[1]
        #getting corp names (for stat report)
        all_names = bib_object.extract_names(transformed)[2]
        corp_names = bib_object.extract_names(transformed)[3]
        print (str(all_names) + " names were extrected from " + filename)
        print (str(len(names)) + " unique names were extracted from " + filename + " --- " + str(len(names) - corp_names) + " Personal names and " + str(corp_names) + " Corporate names")
        print (str(len(titles)) + " titles were extracted from " + filename)
        #dictionaries for storing URIs (names and titles) and stats
        enriched_names = {}
        enriched_titles = {}
        stats = {}
        print ("enriching names")
        # iterate over the name dictionary 
        for index, item in enumerate(names.keys()):
            name = item.split('-_-_-')[0]
            print(index+1, name)
            enriched_names[item] = []
            for api in apis:
                #check if the stat for the API already exists
                if api in stats.keys():
                    pass
                else:
                    stats[api] = 0
                # getting the API method
                name_result = APIFactory().get_API(name, query_type, api, log_file)
                # if the results are not empty, append to "enriched_names" dictionary the result using the api name as key
                if name_result:
                    enriched_names[item].append(name_result)
                    # add number of results to be used latter in stats report
                    stats[api] = stats[api] + len(name_result)
        print ("enriching titles")
        # iterate over the title dictionary
        for index, title in enumerate(titles.keys()):
            print(index+1, title)
            for authors in titles[title]['authors']:
                author =  authors.split('-_-_-')[0]
                key = str(author) + "-_-_-" + str(title)
                enriched_titles[key] = []
                title_result = APIFactory().get_API(author, title, 'search_OCLC', log_file)
                if title_result:
                    enriched_titles[key].append(title_result)
        # getting rid of unwanted things
        name_results = clean_up(enriched_names)
        title_result = clean_up(enriched_titles)
        # get the best URI each API (highest score) and storing it in final_names and final_titles
        result_names_Object = Results(name_results, names, file, 'name', log_file)
        result_names_Object.maximizer()
        final_names = result_names_Object.mapping()
        result_title_Object = Results(title_result, titles, file, 'title', log_file)
        final_titles = result_title_Object.mapping()
        eff = get_stat(final_names, len(names), final_titles, len(titles), filename)
        stats['names-enriched'] = len(final_names)
        tff = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        #write back the URIs to the BIBFRAME file
        write(final_names, final_titles, file, output, log_file, filename)
        tfw = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        write_time = datetime.strptime(tfw, '%H:%M:%S') - datetime.strptime(tff, '%H:%M:%S')
        file_process_time = datetime.strptime(tfw, '%H:%M:%S') - datetime.strptime(tfs, '%H:%M:%S')
        write_stats(eff, stats, filename, len(titles), len(names), all_names, corp_names, file_process_time, write_time)
        #removing temp-file.xml
        delete_temp()
        print(filename + " processed in: ", file_process_time, " --- writing process :", write_time)
    tpf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    process_time = datetime.strptime(tpf, '%H:%M:%S') - datetime.strptime(tps, '%H:%M:%S')
    print("walltime:", process_time)

def write(final_names, final_titles, file, output, log_file, filename):
    folder = 'results'
    if not os.path.exists(folder):
        os.makedirs(folder)
    clear_files(filename)
    print ('writing ' + filename)
    #adding BIBFRAME namespaces
    enhanched = ETree.register_namespace('bf', 'http://id.loc.gov/ontologies/bibframe/')
    enhanched = ETree.register_namespace('bflc', 'http://id.loc.gov/ontologies/bflc/')
    enhanched = ETree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    enhanched = ETree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    enhanched = ETree.register_namespace('madsrdf', 'http://www.loc.gov/mads/rdf/v1#')
    enhanched = ETree.parse(file)
    clear_TSV(filename)
    #writing extract names matching URIs into a TSV file
    tsv_file = 'results/%s/TSVs/URIs-%s.tsv' %(filename, filename)
    with open(tsv_file, "a") as tsv:
        tsv.write("ingest key" + "\t" + "viaf ID" + "\t" + "LC ID" + "\n") 
        print ("writing enriched names")
        for key in final_names.keys():
            name = key.split('-_-_-')[0]
            try:
                #if the key (i.e. LCID or VIAF ID) exists for a certain name, create the URI
                if "LC" in final_names[key]['scores'].keys():
                    LC = 'http://id.loc.gov/authorities/names/' + (final_names[key]['scores']['LC'][0])
                if "VIAF" in final_names[key]['scores'].keys():
                    VF = 'http://viaf.org/viaf/' + (final_names[key]['scores']['VIAF'][0])
                #itterate over the extracted keys (names)
                for k in final_names[key]['keys']:
                    uri_key = k
                    tsv.write(uri_key + "\t" + VF + "\t" + LC + "\n")
                    root = enhanched.getroot()
                    #search the XML for "bf:agent", if the 'example.org' key matches, insert the VF/LC URI
                    for element in root.iter('{http://id.loc.gov/ontologies/bibframe/}Agent'):
                        for ku in element.attrib.keys(): 
                            if element.attrib[ku] == uri_key:
                                element.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', LC)
                                #add the VF element
                                a = ETree.SubElement(element, 'bf:identifiedBy')
                                b = ETree.SubElement(a, 'bf:IdentifiedBy')
                                c = ETree.SubElement(b, 'rdf:value')
                                c.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', VF)
            except:
                print ("could not find identfier for " + key)
                PrintException(log_file, name)
        print ("writing enriched titles")
        #itterate over the extracted keys (titles)
        for title in final_titles.keys():
            try:
                if "oclcid" in final_titles[title]['scores'].keys():
                    OCLC_ID = final_titles[title]['scores']['oclcid'][0]
                if "work_id" in final_titles[title]['scores'].keys():
                    work_ID = final_titles[title]['scores']['work_id'][0]
                for k in final_titles[title]['keys']:
                    uri_key = k
                    tsv.write(uri_key + "\t" + OCLC_ID + "\t" + work_ID + "\n")
                    #search the XML for "bf:Work", if the 'example.org' key matches, insert the OCLC URI
                    root = enhanched.getroot()
                    for element in root.iter('{http://id.loc.gov/ontologies/bibframe/}Work'):
                        for ku in element.attrib.keys(): 
                            if uri_key in element.attrib[ku]:
                                element.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', work_ID)
            except:
                print ("could not find identfier for " + title)
                PrintException(log_file, name)
    out = "results/%s/enhanced-files/%s" %(filename, output)
    enhanched.write(out)

def get_stat(final_names, names, final_titles, titles, file):
    folder = 'results/%s/Diagrams' %(file)
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
    oclcid = 0
    work_id = 0
    LC_Score = []
    VIAF_Score = []
    oclcid_Score = []
    work_id_Score = []
    for i in final_names.keys():
        if "LC" in final_names[i]['scores'].keys():
            LC_Score.append(final_names[i]['scores']['LC'][1])
            LC += 1
        if "VIAF" in final_names[i]['scores'].keys():
            VIAF_Score.append(final_names[i]['scores']['VIAF'][1])
            VIAF += 1
    if len(LC_Score) > 0:
        LC_Avg = statistics.mean(LC_Score)
        LC_Median = statistics.median(LC_Score)
        if len(LC_Score) > 1:
            LC_Var = statistics.variance(LC_Score)
            LC_Std = statistics.stdev(LC_Score)
        else:
            LC_Var = 'N/A'
            LC_Std = 'N/A'
        plt.hist(LC_Score)
        plt.suptitle('Matching Score distribution for LC-IDs (' + file + ')', fontsize=12)
        plt.grid()
        plt.savefig(file_path+"-LC", facecolor='w', edgecolor='w',
            orientation='portrait')
        plt.clf()
        stat['LC'] = [LC, LC_Avg, LC_Median, LC_Var, LC_Std, (LC/names)*100]
    if len(VIAF_Score) > 0:
        VIAF_Avg = statistics.mean(VIAF_Score)
        VIAF_Median = statistics.median(VIAF_Score)
        if len(VIAF_Score) > 1:
            VIAF_Var = statistics.variance(VIAF_Score)
            VIAF_Std = statistics.stdev(VIAF_Score)
        else:
            VIAF_Var = 'N/A'
            VIAF_Std = 'N/A'
        plt.hist(VIAF_Score)
        plt.suptitle('Matching Score distribution for VIAF-IDs (' + file + ')', fontsize=12)
        plt.grid()
        plt.savefig(file_path+"-VIAF", facecolor='w', edgecolor='w',
            orientation='portrait')
        plt.clf()
        stat['VIAF'] = [VIAF, VIAF_Avg, VIAF_Median, VIAF_Var, VIAF_Std, (VIAF/names)*100]
    colors = ['red', 'green']
    labels = ['LC-IDs', 'VIAF-IDs']
    x_multi = [LC_Score, VIAF_Score]
    plt.hist(x_multi, 10, normed=1, histtype='bar', color=colors, label=labels)
    plt.legend(prop={'size': 10})
    plt.suptitle('Matching Score distribution (' + file + ')', fontsize=12)
    plt.savefig(file_path, facecolor='w', edgecolor='w',
        orientation='portrait')
    for i in final_titles.keys():
        if 'work_id' in final_titles[i]['scores']:
            work_id_Score.append(final_titles[i]['scores']['work_id'][1])
            work_id += 1
        if 'oclcid' in final_titles[i]['scores']:
            oclcid_Score.append(final_titles[i]['scores']['oclcid'][1])
            oclcid += 1
    if len(oclcid_Score) > 0:
        oclcid_Avg = statistics.mean(oclcid_Score)
        oclcid_Median = statistics.median(oclcid_Score)
        if len(oclcid_Score) > 1:
            oclcid_Var = statistics.variance(oclcid_Score)
            oclcid_Std = statistics.stdev(oclcid_Score)
        else:
            oclcid_Var = 'N/A'
            oclcid_Std = 'N/A'
        plt.hist(work_id_Score)
        plt.suptitle('Matching Score distribution for OCLC Work IDs (' + file + ')', fontsize=12)
        plt.grid()
        plt.savefig(file_path+"-work_ID", facecolor='w', edgecolor='w',
            orientation='portrait')
        plt.clf()
    if len(work_id_Score) > 0:
        work_id_Avg = statistics.mean(work_id_Score)
        work_id_Median = statistics.median(work_id_Score)
        if len(work_id_Score) > 1:
            work_id_Var = statistics.variance(work_id_Score)
            work_id_Std = statistics.stdev(work_id_Score)
        else:
            work_id_Var = 'N/A'
            work_id_Std = 'N/A'
        plt.hist(oclcid_Score)
        plt.suptitle('Matching Score distribution for OCLC IDs (' + file + ')', fontsize=12)
        plt.grid()
        plt.savefig(file_path+"-oclc_id", facecolor='w', edgecolor='w',
            orientation='portrait')
        plt.clf()
        stat['work_id'] = [work_id, work_id_Avg, work_id_Median, work_id_Var, work_id_Std, (work_id/titles)*100]
        stat['oclcid'] = [oclcid, oclcid_Avg, oclcid_Median, oclcid_Var, oclcid_Std, (oclcid/titles)*100]
    return (stat)

def write_stats(eff, stats, filename, titles, names, all_names, corp_names, process_time, write_time):
    file = filename + "-stats.tsv"
    if not os.path.exists("results/%s/Stats" %(filename)):
        os.makedirs("results/%s/Stats" %(filename))
    file_path = os.path.join("results/%s/Stats" %(filename), file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
    with open(file_path, "w+") as stat:
        stat.write(file + " was processed in " + str(process_time) + " write back to file in " + str(write_time) +"\n\n")
        stat.write(str(all_names) + " names were extracted from " +filename + "\n" + str(names) + " unique names " + " --- " + str(names - int(corp_names)) + " Personal names and " + str(corp_names) + " Corporate names" + "\n")
        stat.write(str(titles) + " titles were extracted from " + filename + "\n\n")
        stat.write("API searched" +"\t" + "hits" + "\t" + "hit_rate" +"\n")
        for i in stats.keys():
            stat.write(i + "\t" + str(stats[i]) + "\t" + str((int(stats[i])/names)*100) + "\n")
        stat.write("\n" + "\n")
        if 'LC' in eff.keys():
            stat.write('LC_ID' + '\n' + "names enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
            for i in eff["LC"]:
                stat.write(str(i) + "\t")
            stat.write("\n" + "\n")
        if 'VIAF' in eff.keys():
            stat.write('VIAF_ID' + '\n' + "names enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
            for i in eff["VIAF"]:
                stat.write(str(i) + "\t")
            stat.write("\n" + "\n")
        if 'work_id' in eff.keys():
            stat.write('work_id' + '\n' + "titles enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
            for i in eff["work_id"]:
                stat.write(str(i) + "\t")
            stat.write("\n" + "\n")
        if 'oclcid' in eff.keys():
            stat.write('oclc_id' + '\n' + "titles enriched" + "\t" + "average matching score" + "\t" + "median matching score" + "\t" + "variance of matching score" + "\t" + "standard-div of matching score" + "\t" + "hit rate" + "\n")
            for i in eff["oclcid"]:
                stat.write(str(i) + "\t")

if __name__ == "__main__":
    main()