#!usr/bin/python3

""" 
a legacy database of "convocation hall" music recordings metadata was converted from MSAccess to a single csv.
data was normalized (open refine) and reconciled using the musicbrainz vocabulary (see import function).
the csv is processed using the rdflib libray and serialized in xml below (see create triples).
"""

import csv
import os
from SPARQLWrapper import SPARQLWrapper
from rdflib import URIRef, Namespace, Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDFS, RDF, DCTERMS
import re
from time import sleep

def main():
    # import_from_music_ontology()
    create_triples()


def import_from_music_ontology():
    """
    takes a list of terms (instruments in this example), 
    queries the musicbrainz vocabulary, outputs txt file with corresponding URI
    """
    
    file = open('instruments.txt')
    search_terms = file.readlines()
    results = []
    for search_term in search_terms:
        payload = {'query': search_term, 'limit': '1', 'fmt':'json'}
        query = 'http://musicbrainz.org/ws/2/instrument?'
        try:
            r = requests.get(query, params=payload).json()
        except:
            pass
        try:
            url = 'musicbrainz.org/instrument/' + r['instruments'][0]['id']
            results.append((r['instruments'][0]['name'], url))
            print((r['instruments'][0]['name'], url))
        except:
            print('empty: ', search_term)
            pass
        sleep(5)
    file.close()
    with open('instrumentLinks.txt', 'w') as fp:
        fp.write('\n'.join('%s %s' % x for x in results))


def create_triples():
    """
    generates an in-memory rdf graph of triples describing 
    the University of Alberta Convocation hall recordings
    exports to a triple store updater function
    """
    
    # instantiate the graph
    g = Graph()  
    
    # musicontology.org namespace assigned to "mo"
    mo = Namespace('http://purl.org/ontology/mo/') 

    # the main data source with reconciled and normalized data
    with open('music.csv') as music_file:
        records = csv.DictReader(music_file)

    # process one line of the combined csv at a time
        for record in records:       
            # process each entity in the entity list
            for entity in record.keys():
                cell_value = record[entity]
                #determine what column this is
                if  entity == 'CompositionNum':
                    # create a composition resource
                    composition = URIRef( "http://library.ualberta.ca/con_hall/Composition/%s" % (cell_value) )
                    # define the resource as a MusicOntology MusicalWork
                    g.add( (composition, RDF.type, mo.MusicalWork) )
                    # label the resource with the title of the composition (a string literal)
                    g.add( (composition, RDFS.label, Literal(str(record['CompositionTitle']))) )
               
                if (entity == 'ComposerURL') & (cell_value != ''):
                    # create a composer resource
                    composer = URIRef( cell_value )
                    # call the compositon resource for linking purposes
                    composition = URIRef( "http://library.ualberta.ca/con_hall/Composition/%s" % (record['CompositionNum']) )
                    # define the resource as a MusicOntology MusicArtist
                    g.add( (composer, RDF.type, mo.MusicArtist) )
                    # give the resource a FOAF name (a string literal)
                    g.add( (composer, FOAF.name, Literal(str(record['ComposerName']))) )
                    # composition is created by composer
                    g.add( (composition, DCTERMS.creator, composer) )
                
                if (entity == 'ComposerNum') & (cell_value != ''):
                    # create a composer resource
                    composer = URIRef( 'http://library.ualberta.ca/con_hall/Composer/%s' % (cell_value) )
                    # call the compositon resource for linking purposes
                    composition = URIRef( "http://library.ualberta.ca/con_hall/Composition/%s" % (record['CompositionNum']) )
                    # define the resource as a MusicOntology MusicArtist
                    g.add( (composer, RDF.type, mo.MusicArtist) )
                    # give the resource a FOAF name (a string literal)
                    g.add( (composer, FOAF.name, Literal(str(record['ComposerName']))) )
                    # composition is created by composer
                    g.add( (composition, DCTERMS.creator, composer) )
                                 
                # recital (i.e. recording) resource and properties
                if entity == 'RecitalNum':
                    recording = URIRef( "http://library.ualberta.ca/con_hall/Recording/%s" % (cell_value) )
                    g.add( (recording, RDF.type, mo.Recording) )
                    g.add( (recording, RDFS.label, Literal(str(record['RecitalName']))) )
                    g.add( (recording, DCTERMS.subject, Literal(str(record['RecitalType']))) )
                    g.add( (recording, DCTERMS.subject, Literal('Convocation Hall')) )
                    g.add( (recording, DCTERMS.date, Literal(str(record['DateRecorded']))) )                        

                # performer (i.e. recording) resource and properties
                if entity == 'PerformerNum':
                    performer = URIRef( "http://library.ualberta.ca/con_hall/Performer/%s" % (cell_value) )
                    g.add( (performer, RDF.type, mo.MusicArtist) )
                    g.add( (performer, FOAF.name, Literal(str(record['PerformerName']))) )
                
                # performance (i.e. recording) resource and properties
                if entity == 'PerformanceNum':
                    performance = URIRef( "http://library.ualberta.ca/con_hall/Performance/%s" % (cell_value) )
                    composition = URIRef("http://library.ualberta.ca/con_hall/Composition/%s" % (record['CompositionNum']) )
                    recording = URIRef("http://library.ualberta.ca/con_hall/Recording/%s" % (record['RecitalNum']) )
                    performer = URIRef("http://library.ualberta.ca/con_hall/Performer/%s" % (record['PerformerNum']) )
                    g.add( (performance, RDF.type, mo.Performance) )
                    # performance performs composition
                    g.add( (performance, mo.performance_of, composition ) )
                    # performance is a part of a recording
                    g.add( (performance, DCTERMS.isPartOf, recording) )
                    # performance has performer
                    g.add( (performer, DCTERMS.isPartOf, performance) )

                # performer role (linked data instance)
                if (entity == 'InstrumentURL')  & (cell_value != ''):
                    performer = URIRef("http://library.ualberta.ca/con_hall/Performer/%s" % (record['PerformerNum']) )
                    performance = URIRef("http://library.ualberta.ca/con_hall/Performance/%s" % (record['PerformanceNum']) )
                    performanceRole = URIRef( str(record[entity]) )
                    g.add( (performanceRole, RDF.type, mo.Instrument) )
                    g.add( (performanceRole, RDFS.label, Literal(str(record['PerformanceLabel']))) )
                    # performer role is attributed both to the performance and to the performer
                    # the role the performer played in a given performance needs to be inferred
                    # a performer's role can potentially be ambiguous
                    g.add( (performance, mo.instrument, performanceRole))
                    g.add( (performer, mo.instrument, performanceRole))
                
                # performer role (literal instance)
                if (entity == 'PerformanceRole') & (cell_value != ''):
                    cell_value = cell_value.replace(' ','_')
                    cell_value = cell_value.replace(',','')
                    performer = URIRef("http://library.ualberta.ca/con_hall/Performer/%s" % (record['PerformerNum']) )
                    performance = URIRef("http://library.ualberta.ca/con_hall/Performance/%s" % (record['PerformanceNum']) )
                    performanceRole = URIRef( "http://library.ualberta.ca/con_hall/Role/%s" % (cell_value) )
                    g.add( (performanceRole, RDFS.label, Literal(str(record['PerformanceLabel']))) )
                    # if the performer role is conductor, this is typed
                    if cell_value == 'conductor':
                        g.add( (performance, mo.conductor, performanceRole) )
                        g.add( (performer, mo.conductor, performanceRole) )
                    else:
                        g.add( (performanceRole, RDF.type, mo.Instrument) )
                        g.add( (performance, mo.instrument, performanceRole) )
                        g.add( (performer, mo.instrument, performanceRole) )
    
    # generates the xml-rdf serialization and exports to file
    g.serialize(destination='con_hall.rdf', format='pretty-xml')
    # appends the generic namespaces with specifics
    with open('con_hall.rdf', 'r') as f:
        ch = f.read()
        ch = ch.replace('ns1','mo').replace('ns2','dcterms').replace('ns3','foaf')
    with open('con_hall.rdf', 'w') as f:
        f.write(ch)

if __name__ == '__main__':
    main()
