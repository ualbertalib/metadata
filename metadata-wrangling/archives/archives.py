#!/usr/bin/env python3

import re
import csv
from html.parser import HTMLParser
import codecs
from bs4 import BeautifulSoup


def main():     
    # initialize a csv file to which we write each row of ATOM data
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = [
                        "filename",
                        "qubit_Parent_Slug", 
                        "title",
                        "rad_General_Material_Designation",
                        "alternate_Title",
                        "level_Of_Description",                   
                        "repository",
                        "creators",
                        "creator_Histories",
                        "creator_Dates",
                        "creator_Dates_Notes",
                        "extent_And_Medium",
                        "archival_History",
                        "scope_And_Content",
                        "arrangement",
                        "language",
                        "access_Conditions",
                        "subject_Access_Points",
                        "place_Access_Points",
                        "name_Access_Points",
                        "institution_Identifier",
                        "revision_History"
                     ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # two text files contain lists of filenames pointing to HTML finding aids
        # the text files are necessary for avoiding many corrupt finding aids
        with open('fondsList.txt', 'r') as f:
            filenames = f.readlines()
            for filename in filenames:
                fondRow = Fonds(filename.strip())
                appendRow(fondRow, writer)
                del(fondRow)
                
        with open('seriesList.txt', 'r') as f:
            filenames = f.readlines()
            for filename in filenames:                    
                seriesRow = Series(filename.strip())
                appendRow(seriesRow, writer)
                # file data is found in the Series HTML and is thus logically nested
                # iterate over file data as single rows
                for fileRow in seriesRow.fileCollection:
                    appendRow(fileRow, writer)
                del(seriesRow)


def appendRow(newRow, writer):    
    # writes to the csv file
    writer.writerow( {  
                        "filename": newRow.filename,
                        "qubit_Parent_Slug": newRow.qubit_Parent_Slug, 
                        "title": newRow.title,
                        "rad_General_Material_Designation": newRow.rad_General_Material_Designation,
                        "alternate_Title": newRow.alternate_Title,
                        "level_Of_Description": newRow.level_Of_Description,
                        "repository": newRow.repository,
                        "creators": newRow.creators,
                        "creator_Histories": newRow.creator_Histories,
                        "creator_Dates": newRow.creator_Dates,
                        "creator_Dates_Notes": newRow.creator_Dates_Notes,
                        "extent_And_Medium": newRow.extent_And_Medium,
                        "archival_History": newRow.archival_History,
                        "scope_And_Content": newRow.scope_And_Content,
                        "arrangement": newRow.arrangement,
                        "language": newRow.language,
                        "access_Conditions": newRow.access_Conditions,
                        "subject_Access_Points": newRow.subject_Access_Points,
                        "place_Access_Points": newRow.place_Access_Points,
                        "name_Access_Points": newRow.name_Access_Points,
                        "institution_Identifier": newRow.institution_Identifier,
                        "revision_History": newRow.revision_History
                     }
                   )


class TAGStripper(HTMLParser):
    
    """HTML tag remover for cleanly parsing HTML"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = TAGStripper()
    s.feed(html)
    return s.get_data()


class Record(object):

    """HTML input, parses into ATOM fields as a complete ATOM record"""
    
    def __init__(self, filename):       
        self.filename = filename
        with codecs.open(self.filename, "r",encoding='utf-8', errors='ignore') as fdata:
            self.soup = BeautifulSoup(fdata, 'lxml')
        self.creator_Dates = ""
        self.extent_And_Medium = ""
        self.scope_And_Content = ""
        self.title = ""
        self.rad_General_Material_Designation = ""
        self.alternate_Title = ""
        self.qubit_Parent_Slug = ""       
        self.creators = ""
        self.level_Of_Description = ""
        self.repository = ""
        self.creator_Histories = ""
        self.creator_Dates_Notes = ""
        self.archival_History = ""
        self.arrangement = ""
        self.language = ""
        self.access_Conditions = ""
        self.subject_Access_Points = ""
        self.place_Access_Points = ""
        self.name_Access_Points = ""
        self.institution_Identifier = ""
        self.revision_History = "" 
        self.data = self.soup.find('div',id='did')
        if self.data is None:
            self.data = self.soup.find('td',id='main')

    def __del__(self): pass


class Fonds(Record):
    
    """Fonds specific ATOM record"""
    
    # initalize fonds variables and call scraper methods
    def __init__(self, filename):
        super(Fonds, self).__init__(filename)
        self.level_Of_Description = "fonds"
        self.repository = "University Archives"
        self.language = "English"
        self.institution_Identifier = "AEU"
        self.revision_History = re.sub('(\s)+',' ',strip_tags(str(self.soup.find('td', id='institute'))))
   
    # scraping data from HTML and cleanup 
        try:
            for content in self.data.contents:
                if re.search(r'records|audio|material|sound|recordings|media|textual|photographs|metre', str(content), re.IGNORECASE) is not None:
                    self.rad_General_Material_Designation = self.rad_General_Material_Designation + str(content.strip()) + '\n'
                    self.rad_General_Material_Designation = self.rad_General_Material_Designation.strip()
        except:
            pass
        
        try:
            for content in self.data.contents:
                if re.search(r'acc', str(content), re.IGNORECASE) is not None:   
                    self.alternate_Title = content.strip()
                    break
        except:
            pass
    
        try:
            for content in self.data.contents:
                if re.search(r'Fonds|Collection|Archives', str(content), re.IGNORECASE) is not None:
                    self.title = content.strip()
                    break
        except:
            pass
    
        try:
            for content in self.data.contents:
                if re.search(r'ACC', str(content), re.IGNORECASE) is not None:
                    pass
                elif re.search(r'[12][78901][0-9]{2}', str(content)) is not None:
                    self.creator_Dates = content.strip()
                    break
        except:
            pass
    
        try:
            for content in self.data.contents:
                if re.search(r'records|audio|material|sound|recordings|media|textual|photographs|metre', str(content), re.IGNORECASE) is not None:
                    self.extent_And_Medium = self.extent_And_Medium + str(content.strip()) + '\n'
                    self.extent_And_Medium.strip()
        except:
            pass  
    
        if re.search(r"<a name=\"scope\">Scope and Content</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL) is not None:
            self.scope_And_Content = strip_tags(re.sub('(\s)+',' ',str(re.search(r"<a name=\"scope\">Scope and Content</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL).groups(0)[0])))   
        if re.search(r"<a name=\"biography\">.+?</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL) is not None:
            self.creator_Histories = strip_tags(re.sub('(\s)+',' ',str(re.search(r"<a name=\"biography\">.+?</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL).groups(0)[0])))
        if re.search(r"<a name=\"custohist\">Custodial History</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL) is not None:
            self.archival_History = strip_tags(re.sub('(\s)+',' ',str(re.search(r"<a name=\"custohist\">Custodial History</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL).groups(0)[0])))    
        if re.search(r"<a name=\"arrangement\">.+?</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL) is not None:
            self.arrangement = strip_tags(re.sub('(\s)+',' ',str(re.search(r"<a name=\"arrangement\">.+?</a>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL).groups(0)[0])))
        if re.search(r"<h4>Restrictions on Access</h4>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL) is not None:
            self.access_Conditions = strip_tags(re.sub('(\s)+',' ',str(re.search(r"<h4>Restrictions on Access</h4>(.+?)?<hr size=\"1\"/>", str(self.soup), re.DOTALL).groups(0)[0])))
        self.creators = re.sub(r'(Fonds|Collection|Archives|fonds|collection|archives)', '', self.title, re.IGNORECASE).strip()


class Series(Record):

    """series specific ATOM record"""
    
    def __init__(self, filename):
        super(Series, self).__init__(filename)
        self.level_Of_Description = "series"
        self.fileCollection = []
        
        # scraping data from HTML and cleanup         
        for content in self.data.find(id='series'):
            if re.search("\W(.*?)[.][-]", str(content)) is not None:
                self.title = re.search("\W(.*?)[.]--", str(content)).groups(0)[0]
            break              
        for content in self.data.find(id='series'):
            if re.search("[-].(.+).[-]", str(content)) is not None:
                self.creator_Dates = re.search(r'[-].(.+).[-]', str(content)).groups(0)[0]
            break
        for content in self.data.find(id='series'):
            if re.search(r'([-])+(.+)([-])(.+)', str(content), re.IGNORECASE) is not None:
                self.extent_And_Medium = re.search(r'([-])+(.+)([-])(.+)', str(content)).groups(0)[3]
            break
        if self.data.p is not None:
            self.scope_And_Content = re.sub('(\s)+',' ',str(self.data.p.string)).strip()
        # special method, iterates over each file in the series
        # passes data to a new file object
        # stores object in a local (series level) list
        for listings in self.data.find_all(id='filelisting'):
            newFile = File(self.filename.strip(), listings)
            self.fileCollection.append(newFile)


class File(Record):
    
    """file specific ATOM record"""
    
    def __init__(self, filename, listings):
        super(File, self).__init__(filename)
        self.level_Of_Description = "file"
        self.listings = listings
                
        # parses and writes row data to the file object
        self.alternate_Title = str(self.listings.contents[1].string) + ' ' + str(self.listings.contents[3].string)
        self.alternate_Title = self.alternate_Title.replace('None','').strip()
        self.title = str(re.sub( '(\s)+', ' ', str(self.listings.contents[5].string) )).replace('None','')
        self.creator_Dates = str(self.listings.contents[7].string)          


if __name__ == '__main__':
    main()