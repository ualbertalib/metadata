#!/usr/bin/env

# Modules ########################################################################################

import os
import csv
import re
import sys
import traceback

# Init ###########################################################################################

# filenames
filesStub = []

# database dictionaries
mimsyData = {}
imageData = {}

# for writing to a batch csv
output = []
fieldnames =["fileName", "itemType", "ownerId", "isVersionOf", "title", "creator", "contributor", "description", "subject",
             "license", "rights", "dateCreated", "language","relatedURL", "source", "temporal", "spatial", "embargoDate",
             "visOnIngest", "visAfterEmbargo", "communityName", "communityNoId", "collectionName", "collectionNoId"]

# Notes ###########################################################################################

# Purpose: Harvests data from a document of extracted image metadata and a
# csv of metadata from the mimsy database of #archaeological objects. This
# harvested data is mapped to a metadata schema designed for batch ingest
# into Hydra. #Metadata is matched to the appropriate object filename in
# the local directory and written to a csv for eventual ingest.

# Object files not found in the mimsy database (by file name):
# 1970-020-011ab_d, 1970-020-007_v, 1970-020-010_d, 1970-020-007_d,
# 1970-020-005_d, 1970-020-009_d, 1970-020-010_v, #1970-020-008_v,
# 1970-020-006_v, 1970-020-006_d, 1970-020-005_v, 1970-020-009_v,
# 1970-020-008_d

# Object files where no metadata was extracted:
# 1970-086-003, 1970-086-002, 1970-086-005, 1994-035-001_d,
# 1970-086-001lot, 1970-086-006, 1970-086-004, 1970-086-001_d,
# #1970-068-001lot, 1994-035-005_d, 1994-035-006_d, 1994-035-001lot,
# 1994-035-004_d, 1994-035-002_d, 1994-035-003_d, #1970-018-016,
# 1970-018-017

# Data Transfer & Testing############################################################################

# tests and issues report on:
# 1) total number of objects,
# 2) total number of objects matched in the mimsy database,
# 3) total number of objects with extracted metadata
# packages matching data and unmatched data separately and passes them on


def dataTransferObject(imageData, mimsyData):

    images = 0
    mimsies = 0
    flagImageData = "F"
    flagMimsyData = "T"
    missedMimsyData = []
    missedImageData = []

    # iterates over filenames
    print (len(filesStub))
    for fileName in filesStub:

        # checks image metadata inventory for a match and flags true if found
        if fileName in imageData.keys():
            images = images + 1
            flagImageData = "T"

        # checks mimsy database inventory for a match and flags true if found
        if fileName in mimsyData.keys():
            mimsies = mimsies + 1
            flagMimsyData = "T"

        # adds the object name to a list of missed objects if a flag wasn't raised
        if flagMimsyData == "F":
            missedMimsyData.append(fileName)
        if flagImageData == "F":
            missedImageData.append(fileName)

        # flags reset
        flagImageData, flagMimsyData = "F", "F"

    # report issued (uncomment to activate)
    print("number of files processed: ", len(filesStub))
    print("number of Mimsy database metadata processed:", mimsies)
    print("number of image metadata processed:", images)
    # print("missed mimsies: ", missedMimsyData)
    # print('\n')
    # print("missed imagedatas: ",missedImageData)

    return({'mimsyData': mimsyData, 'imageData': imageData, 'missedMimsyData': missedMimsyData, 'missedImageData': missedImageData})

# reusable error traceback module with line number callback


def error(source):
    print("Exception in user code", source)
    print('-' * 60)
    traceback.print_exc(file=sys.stdout)
    print('-' * 60)

# etadata Getters and Setters#######################################M#####################################

# sets a list of file names for every object in the file tree ending in .TIF


def setFileData():
    count = 0
    for directory in os.listdir("Sample/files/"):
        for f in os.listdir("Sample/files/" + directory):
            if f.endswith(".tif") | f.endswith(".TIF"):
                count = count + 1
                try:
                    filesStub.append(resolveNames(f, 'file'))
                except:
                    error('file list')

    print('number of files pre-processed: ', count)
    return filesStub

# sets


def setImageData():
    try:
        with open('output.txt', 'r') as f:
            metadata = f.readlines()
        for line in metadata:
            if "Image: " in line:
                imageData[resolveNames(line, "imageData")] = {}
                image = resolveNames(line, "imageData")
            if "date:modify" in line:
                imageData[image]['date'] = re.sub('date: ', '', re.sub("\\n", "", re.sub(":modify", "", re.sub("(^.\s+)", "", line, re.MULTILINE))))
            if "Image Name[2,5]" in line:
                temp = re.sub("\\n", "", re.sub("(^.\s+)", "", line, re.MULTILINE))
                imageData[image]['title'] = re.sub('Image Name\[2,5\]: ', '', temp)
            if "Byline[2,80]" in line:
                temp = re.sub("\\n", "", re.sub("(^.\s+)", "", line, re.MULTILINE))
                imageData[image]['creator'] = re.sub('Byline\[2,80\]: ', '', temp)
        return imageData
    except:
        error('image metadata')


def setMimsyData():
    try:
        with open("Sample/Processing/Mimsy_2013/2013.csv", newline='') as csvfile:

            reader = csv.DictReader(csvfile)
            mimsyData = {}
            for row in reader:
                resolvedName = resolveNames(row['id'], "mimsyData")

                # if len(row['id'])>13: ID = row['id'][0:13]
                # else: ID = row['id'][0:12]

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
    except:
        error('mimsy metadata')


def getTitle(mimsy, image, fileName):
    try:
        if 'title' in image.keys():
            title = image['title']
        else:
            title = mimsy['accession']  # accesssion
            if fileName.find('v_') > -1:
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
        return title
    except:
        error('title data')

# def getSuper(source, MDType):
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
        if mimsy['maker'] == 'unknown':
            return "© University of Alberta, Department of Anthropology"
        else:
            return '© University of Alberta, Department of Anthropology,  Specimen © ' + mimsy['maker']
    except:
        error('rights data')


def getContributor(mimsy):
    try:
        if mimsy['maker'] == 'unknown':
            return "© University of Alberta, Department of Anthropology"
        else:
            return mimsy['maker']
    except:
        error('contributor data')


def getCreator(image):
    try:
        if 'creator' in image:
            return image['creator']
        else:
            return 'University of Alberta Department of Anthropology'
    except:
        print('creator data')


def getDate(image):
    try:
        if 'date' in image:
            return image['date']
        else:
            return ''
    except:
        error('creator date data')

# Helpers################################################################################

# maps object names to a common naming schema


def resolveNames(objectName, Type):
    match = ''
    flag = 'T'
    # strips, cases, and removes path & extension from filename
    objectName = objectName.lower().strip()

    if 'mimsyData' not in Type:
        objectName = re.search('(.+/{1}|(^))(.+)\.tif', objectName).group(3)

    # converts all names from inconsistent use of dashes and period delimiters to a consistant use of dash delimiters
    objectName = re.sub('([.]+)', '-', objectName)

    # strips any trailing underscores
    if objectName.endswith('_'):
        objectName = objectName.rstrip('_')

    # catch-all regex for resolving object names according to 11 existing name variations. If names were passed directly,
    # we would not be able to treat file names as unique identifiers for use in the database. With an updated mimsy
    # database, new failed mimsy matches will require adjustments or additions to this regex. Consider it the botteneck in
    # the script.
    resolvedObjectName = re.search('(^[-.0-9]+[_]?[0-9]?)$|(^[-.0-9]{12}[_|rl]*)$|(^[-.0-9]{12}[ab]*_d)$|(^[-.0-9]+[-_a-z]*)_[vs][0-9][0-9]*|(^[-+0-9]{12}_\w)[_\W]|(.+lot)|(^[0-9][0-9]?-[0-9][0-9]?$)|(589-[-0-9]{7}_\D)|(2011_1_1)production_3years_aug93|(.+[.]pdf)|(^(2005|2011).+)|(^[-.0-9]+[_]?[\D]?[_]?[\D])[\D]*$|^[-0-9]_and.*', objectName)

    # tests that the regex resolved the name for one of the 11 known matches and passes the match on, otherwise throws a
    # message

    if resolvedObjectName:
        flag = 'F'
        for i in range(1, 14):
            if resolvedObjectName.group(i) is not None:
                flag = 'T'
                match = resolvedObjectName.group(i)

    if flag == 'F':
        print(objectName)

    return match


# Maps metadata to a csv dictionary which is passed to the writer object
def mapper(missedMimsies, missedImageD, mimsy, image, fileName):

    # maps database agnostic metadata fields
    row = {}
    row['fileName'] = fileName
    row['itemType'] = "Image"  # itemType
    row['ownerId'] = ""  # ownerId
    row['isVersionOf'] = ""  # isVersionOf
    row['license'] = ''  # license
    row['language'] = "No linguistic content"  # language
    row['relatedURL'] = ''  # relatedURL
    row['source'] = "Bryan/Gruhn Archaeology Collection, Department of Anthropology, University of Alberta"  # source
    row['embargoDate'] = ""  # embargoDate
    row['visOnIngest'] = "Open Access"  # visOnIngest
    row['visAfterEmbargo'] = ""  # visAfterEmbargo
    row['communityName'] = "Department of Anthropology"  # communityName
    row['communityNoId'] = "44558r023"  # communityNoId
    row['collectionName'] = "Bryan/Gruhn Archaeology Collection"  # collectionName
    row['collectionNoId'] = "44558t46k"  # collectionNoId

    # maps fields requiring both image and mimsy metadata
    if (fileName) and (fileName not in missedImageD) and (fileName not in missedMimsies):
        row['title'] = getTitle(mimsy[fileName], image[fileName], fileName)

    # maps fields requiring only image metadata
    if (fileName) and (fileName not in missedImageD):
        row['dateCreated'] = getDate(image[fileName])  # date
        row['creator'] = getCreator(image[fileName])

    # we would not be able to treat file names as unique identifiers for use in the database. With an updated mimsy
    # maps fields requiring only mimsy metadata
    if (fileName) and (fileName not in missedMimsies):
        row['contributor'] = getContributor(mimsy[fileName])  # contributor
        row['description'] = mimsy[fileName]['count'] + ' ' + mimsy[fileName]['object']  # description (count + object)
        subject = mimsy[fileName]['category'] + '|' + mimsy[fileName]['culture'] + '|' + mimsy[fileName]['geo_culture']
        row['subject'] = re.sub("[\|]$", "", subject.replace('||', '|'))  # subject (category,culture, geo_culture)
        row['rights'] = getRights(mimsy[fileName])  # rights
        # temporal =  mimsy[fileName]['geo_culture'] + '|' + mimsy[fileName]['period']
        # row['temporal'] = re.sub('[\|]$','',temporal.replace('||','|')) #temporal (geo_culture, period)
        row['temporal'] = mimsy[fileName]['period']
        row['spatial'] = re.sub('^.+[:] ', '', mimsy[fileName]['place']).replace(', ', '|')  # spatial (place)

    return row


# Combines data and outputs to csv
def combineOutput(csv_file, fileStub, data):
    rowCount = 0
    missedMimsyData, missedImageData, mimsyData, imageData = data['missedMimsyData'], data['missedImageData'], data['mimsyData'], data['imageData']

    for fileName in filesStub:
        output.append(mapper(missedMimsyData, missedImageData, mimsyData, imageData, fileName))
        if isinstance(fileName,type) is not None:
            rowCount = rowCount + 1

    with open(csv_file, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(output)

    print('Total rows of metadata written to CSV: ', rowCount)
    print('Total elements of metadata written to CSV: ', rowCount * len(fieldnames))


# Main Init Module
def main(csv_file): combineOutput(csv_file, setFileData(), dataTransferObject(setImageData(), setMimsyData()))


if __name__ == "__main__":
    main(csv_file)
