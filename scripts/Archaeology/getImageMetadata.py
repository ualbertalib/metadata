#!/usr/bin/env
import re
import csv
imageData = {}
date = ''
title = ''
creator = ''
image = ''

with open('output.txt', 'r') as f: metadata = f.readlines()

for line in metadata:    
    if "Image: " in line:
        image = re.sub(".+/","",re.sub(".tif|.TIF","",re.sub("\.","-",re.sub("Image:","",re.sub("\n","",re.sub("(^.\s+)","",line, re.MULTILINE)))))).strip().lower()
    if "date:modify" in line: date = re.sub('date: ','',re.sub("\\n","",re.sub(":modify","",re.sub("(^.\s+)","",line, re.MULTILINE))))
    if "Image Name[2,5]" in line: title = re.sub('Image Name\[2,5\]: ','',re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE)))
    if "Byline[2,80]" in line: creator = re.sub('Byline\[2,80\]: ','',re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE)))
    if "http://www.imagemagick.org" in line:
        if image!='': 
            imageData[image[0:14]] = {}
            imageData[image[0:14]]['date'] = date
            imageData[image[0:14]]['title'] = title
            imageData[image[0:14]]['creator'] = creator

        date = ''
        title = ''
        creator = ''
        

with open('imageMetadata.csv', 'w') as csvfile:
    fieldnames = ['id','title','date','creator']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for x in imageData: writer.writerow({'id': x, 'title': imageData[x]['title'],'date': imageData[x]['date'],'creator': imageData[x]['creator'] })
