#!/usr/bin/env

###########################################Modules#################################################

import os
import csv
import re
import sys
import traceback

############################################Init###################################################

#filenames
filesStub = []
duplicated = []

#database dictionaries
mimsyData = {}
imageData = {}

#for writing to a batch csv
output = []
fieldnames = ["fileName","title","creator","contributor","description","subject","rights","dateCreated","source","temporal","spatial","maker","communityName","communityNoId","collectionName","collectionNoId"]
############################################Notes##################################################

#Purpose: Harvests data from a document of extracted image metadata and a csv of metadata from the mimsy database of #archaeological objects. This harvested data is mapped to a metadata schema designed for batch ingest into Hydra. #Metadata is matched to the appropriate object filename in the local directory and written to a csv for eventual ingest.

#Object files not found in the mimsy database (by file name):
#1970-020-011ab_d, 1970-020-007_v, 1970-020-010_d, 1970-020-007_d, 1970-020-005_d, 1970-020-009_d, 1970-020-010_v, #1970-020-008_v, 1970-020-006_v, 1970-020-006_d, 1970-020-005_v, 1970-020-009_v, 1970-020-008_d

#Object files where no metadata was extracted:
#1970-086-003, 1970-086-002, 1970-086-005, 1994-035-001_d, 1970-086-001lot, 1970-086-006, 1970-086-004, 1970-086-001_d, #1970-068-001lot, 1994-035-005_d, 1994-035-006_d, 1994-035-001lot, 1994-035-004_d, 1994-035-002_d, 1994-035-003_d, #1970-018-016, 1970-018-017

########################################Data Transfer & Testing#############################################

#tests and issues report on: 
#1) total number of objects, 
#2) total number of objects matched in the mimsy database, 
#3) total number of objects with extracted metadata
#packages matching data and unmatched data separately and passes them on
def dataTransferObject(imageData,mimsyData):

    images = 0
    mimsies = 0  
    flagImageData = "F"
    flagMimsyData = "T"
    missedMimsyData = []
    missedMimsys = []
    missedImageData = []  
    
    #iterates over filenames
    for fileName in filesStub:
        
        #checks image metadata inventory for a match and flags true if found
        if fileName[0] in imageData.keys(): 
            images = images + 1
            flagImageData = "T"
        
        #checks mimsy database inventory for a match and flags true if found
        if fileName[0] in mimsyData.keys():
            mimsies = mimsies + 1
            flagMimsyData = "T"
        
        #adds the object name to a list of missed objects if a flag wasn't raised
        if flagMimsyData == "F":
            missedMimsyData.append(fileName[0])
            missedMimsys.append(fileName[1])

        if flagImageData == "F": missedImageData.append(fileName[0])
        
        #flags reset
        flagImageData,flagMimsyData = "F","F"  

    #report issued (uncomment to activate)
    print("number of files processed: ",len(filesStub))
    print("number of Mimsy database metadata processed:", mimsies)
    print("number of image metadata processed:", images)
    print("missed mimsies: ", len(missedMimsyData))
    #print('\n')
    #print("missed imagedatas: ",missedImageData)
    with open('no-mimsy.txt', 'w+') as mim:
        for item in missedMimsys:
            mim.write(str(item) +'\n')
        mim.close()
    
    return({'mimsyData':mimsyData, 'imageData': imageData, 'missedMimsyData': missedMimsyData, 'missedImageData': missedImageData})

#reusable error traceback module with line number callback
def error(source): 
    print("Exception in user code",source)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)  

########################################Metadata Getters and Setters#####################################

#sets a list of file names for every object in the file tree ending in .TIF
def setFileData():
    count = 0
    for directory in os.listdir("Sample/files/"):
        for f in os.listdir("Sample/files/" + directory):
            if f.endswith(".tif")|f.endswith(".TIF"):
                count = count + 1
                try:
                    file = resolveNames(f,'file')
                    if (file, f) in filesStub:
                        duplicated.append((directory, file))
                    else:
                        filesStub.append( (file, f) )
                except: error('file list')

    print('number of files pre-processed: ', count)
    with open('duplicated.txt', 'w+') as dup:
        for item in duplicated:
            dup.write(str(item) +'\n')
        dup.close()

    return filesStub

# sets extracted metadata derived from the metadata extraction document
def setImageData():
    try:
        with open('output.txt', 'r') as f: metadata = f.readlines()
        for line in metadata:    
            if "Image: " in line: 
                imageData[resolveNames(line.replace("Image: ", ""),"imageData")] = {}
                image = resolveNames(line.replace("Image: ", ""),"imageData")
            if "date:modify" in line: imageData[image]['date'] = re.sub('date: ','',re.sub("\\n","",re.sub(":modify","",re.sub("(^.\s+)","",line, re.MULTILINE))))
            if "Image Name[2,5]" in line:
                temp = re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE))
                imageData[image]['title'] = re.sub('Image Name\[2,5\]: ','',temp)
            elif "filename:" in line:
                if 'title' in imageData[image].keys():
                    pass
                else:
                    temp = re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE))
                    imageData[image]['title'] = re.sub('filename: ','',temp).replace('.tif', '')
            if "Byline[2,80]" in line: 
                temp = re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE))
                imageData[image]['creator'] = re.sub('Byline\[2,80\]: ','',temp)     
        return imageData
    except: error('image metadata')

#extracts data from mimsy csv and assigns to a list
def setMimsyData():
    try:
        with open("Sample/Processing/Mimsy_2015/2015.csv", newline='') as csvfile:            
            reader = csv.DictReader(csvfile)
            mimsyData = {}
            for row in reader:
                resolvedName = resolveNames(row['id'],"mimsyData")              
                mimsyData[resolvedName] = {}
                mimsyData[resolvedName]['accession'] = row['accession']
                mimsyData[resolvedName]['object'] = row["object"]
                mimsyData[resolvedName]['count'] = row["count"]
                mimsyData[resolvedName]['category'] = row["category"]
                mimsyData[resolvedName]['sub_category'] = row["sub_category"]
                mimsyData[resolvedName]['culture'] = row["culture"]
                mimsyData[resolvedName]['geo_culture'] = row["geo_culture"]
                mimsyData[resolvedName]['period'] = row["period"]
                mimsyData[resolvedName]['place'] = row["place"]
                mimsyData[resolvedName]['source'] = row["source"]
                mimsyData[resolvedName]['maker'] = row["maker"]
            return(mimsyData)
    except: error('mimsy metadata')

#tests for what kind of title to make this                
def getTitle(mimsy,image,fileName): 
    title = None
    try:
        if 'title' in image.keys():
            title = image['title'].split('_')[0]
            if fileName.find('v') > -1:
                    title = title + ' ventral'
            elif fileName.find('d') > -1:
                title = title + ' dorsal'
            elif fileName.find('p') > -1:
                title = title + ' proximal'
            elif fileName.find('dt') > -1:
                title = title + ' distal'
            elif fileName.find('rl') > -1:
                title = title + ' right lateral'
            elif fileName.find('ll') > -1:
                title = title + ' left lateral'
            elif fileName.find('LOT') > -1:
                title = 'View of a lot of ' + mimsy['category'].rstrip('s') + ' specimans'            
        else:
            if 'accession' in mimsy.keys():
                title = mimsy['accession'] #accesssion
                if fileName[0].find('v_')>-1: title = title + ' ventral'
                elif fileName[0].find('d')>-1: title = title + ' dorsal'
                elif fileName[0].find('p')>-1: title = title + ' proximal'
                elif fileName[0].find('dt')>-1: title = title + ' distal'
                elif fileName[0].find('rl')>-1: title = title + ' right lateral'
                elif fileName[0].find('ll')>-1: title = title + ' left lateral'    
                elif fileName[0].find('LOT')>-1: title = 'View of a lot of ' + mimsy['category'].rstrip('s') + ' specimans'
        return title
    except: error('title data')

#def getSuper(source, MDType):
#    if 'maker' in source.keys():
#        if 'unknown' in source.keys['maker']: return "© University of Alberta, Department of Anthropology"
#        if source['maker']!='unknown':
#            if MDType="rights": 
#                return '© University of Alberta, Department of Anthropology,  Specimen © ' + mimsy['maker']
#            if MDType="contributor": 
#                return mimsy['maker']
#    if 'date' in source.keys():
#        if  in source: return source[MDType]
#        elif MDType == 'creator': return 'University of Alberta Department of Anthropology'
#        elif MDType == 'date': return ''
        
def getRights(mimsy):
    try:
        if mimsy['maker']=='unknown':
            return "© University of Alberta, Department of Anthropology"
        else: 
            return '© University of Alberta, Department of Anthropology,  Specimen © ' + mimsy['maker']
    except: error('rights data')
        
def getContributor(mimsy):
    try:
        if mimsy['source'] !='':
            return mimsy['source']
        else:
            return "© University of Alberta, Department of Anthropology"
    except: error('contributor data')
        
def getCreator(image):
    try:
        if 'creator' in image: 
            return image['creator']
        else:
            return 'University of Alberta Department of Anthropology'
    except: print('creator data')
        
def getDate(image):
    try:
        if 'date' in image: 
            return image['date'].split('T')[0]
        else: 
            return ''
    except: error('creator date data')

########################################Maps & Resolvers############################################
    
#maps object names to a common naming schema
def resolveNames(objectName,Type):
    match = ''
    flag = 'T'
    #strips, cases, and removes path & extension from filename 
    objectName = objectName.lower().strip()

    if 'mimsyData' not in Type: objectName = re.search('(.+/{1}|(^))(.+)\.tif',objectName).group(3)
    
    #converts all names from inconsistent use of dashes and period delimiters to a consistant use of dash delimiters
    objectName = re.sub('([.]+)','-',objectName)
    
    #strips any trailing underscores
    if objectName.endswith('_'): objectName = objectName.rstrip('_')
    
    #catch-all regex for resolving object names according to 11 existing name variations. If names were passed directly, 
    #we would not be able to treat file names as unique identifiers for use in the database. With an updated mimsy 
    #database, new failed mimsy matches will require adjustments or additions to this regex. Consider it the botteneck in 
    #the script.
    resolvedObjectName = re.search('(^[-.0-9]+[_]?[0-9]?)$|(^[-.0-9]{12}[_|rl]*)$|(^[-.0-9]{12}[ab]*_d)$|(^[-.0-9]+[-_a-z]*)_[vs][0-9][0-9]*|(^[-+0-9]{12}_\w)[_\W]|(.+lot)|(^[0-9][0-9]?-[0-9][0-9]?$)|(589-[-0-9]{7}_\D)|(2011_1_1)production_3years_aug93|(.+[.]pdf)|(^(2005|2011).+)|(^[-.0-9]+[_]?[\D]?[_]?[\D])[\D]*$|^[-0-9]_and.*',objectName)
    
    #tests that the regex resolved the name for one of the 11 known matches and passes the match on, otherwise throws a 
    #message
    
    if resolvedObjectName:
        flag = 'F'
        for i in range(1,14):
            if resolvedObjectName.group(i) is not None: 
                flag = 'T'
                match = resolvedObjectName.group(i)
    
    if flag == 'F': print(objectName)
    if match == '':
        match = objectName

    return match
    
        
#Maps metadata to a csv dictionary which is passed to the writer object
def mapFields(missedMimsies,missedImageD,mimsy,image,fileName):
    
    #maps database agnostic metadata fields
    dummy = {'dummy': 'dummy'}
    row = {}
    row['fileName'] = fileName[1].replace('.tif', '').replace('.TIF', '')
    row['title'] = ""
    row['maker'] = ""
    row['source'] = mimsy[fileName[0]]['source'] #source
    row['communityName'] = "Department of Anthropology" #communityName
    row['communityNoId'] = "44558r023" #communityNoId
    row['collectionName'] = "Bryan/Gruhn Archaeology Collection" #collectionName
    row['collectionNoId'] = "44558t46k" #collectionNoId

    #maps fields requiring both image and mimsy metadata
    if (fileName[0]) and (fileName[0] not in missedImageD) and (fileName[0] not in missedMimsies):
        row['title'] = getTitle(mimsy[fileName[0]],image[fileName[0]],fileName[0])
        row['dateCreated'] = getDate(image[fileName[0]]) #date      
        row['creator'] = getCreator(image[fileName[0]])
 
    #maps fields requiring only image metadata
    '''if (fileName[0]) and (fileName[0] not in missedImageD):
        if row['title'] == "":
            row['title'] = getTitle(dummy,image[fileName[0]],fileName[0])
        row['dateCreated'] = getDate(image[fileName[0]]) #date      
        row['creator'] = getCreator(image[fileName[0]])'''
    
    #we would not be able to treat file names as unique identifiers for use in the database. With an updated mimsy 
    #maps fields requiring only mimsy metadata
    if (fileName[0]) and (fileName[0] not in missedMimsies):
        if row['title'] == "":
            row['title'] = getTitle(mimsy[fileName[0]],dummy,fileName[0])
        row['contributor'] = getContributor(mimsy[fileName[0]]) #contributor
        row['description'] = mimsy[fileName[0]]['count'] + ' ' + mimsy[fileName[0]]['object'] #description (count + object)
        subject = mimsy[fileName[0]]['category'] + '|' + mimsy[fileName[0]]['sub_category'] 
        row['subject'] = re.sub("[\|]$","",subject.replace('||','|')) #subject (category,culture, geo_culture)      
        row['rights'] = getRights(mimsy[fileName[0]]) #rights
        row['temporal'] = "%s|%s" %(mimsy[fileName[0]]['period'], mimsy[fileName[0]]['culture']) # temporal (period, culture)
        row['spatial'] = "%s|%s" %(re.sub('^.+[:] ','',mimsy[fileName[0]]['place']).replace(', ', '|'), re.sub('^.+[:] ','',mimsy[fileName[0]]['geo_culture']).replace(', ', '|')) #spatial (place, geo_culture)     
        row['maker'] = mimsy[fileName[0]]['maker']
    
    return row

#Combines data and outputs to csv
def combineOutput(csv_file, filesStub,data):
    rowCount = 0
    missedMimsyData,missedImageData,mimsyData,imageData = data['missedMimsyData'],data['missedImageData'],data['mimsyData'],data['imageData']
  
    for fileName in filesStub:
        if fileName[0] not in missedMimsyData:
            output.append(mapFields(missedMimsyData,missedImageData,mimsyData,imageData,fileName))
            if fileName[0] is not type(None): 
                rowCount = rowCount + 1

    with open(csv_file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames = fieldnames )
        dict_writer.writeheader()
        dict_writer.writerows(output)

    print('Total rows of metadata written to CSV: ', rowCount)
    print('Total elements of metadata written to CSV: ', rowCount * len(fieldnames) )

    
#Main Init Module
def main(csv_file): combineOutput(csv_file, setFileData(),dataTransferObject(setImageData(),setMimsyData()))

        

if __name__ == "__main__": main()  
