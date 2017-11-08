from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
import datetime
import re
app = Flask(__name__)
sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
sparql.setReturnFormat(JSON)



@app.route('/_getProperties')
def _getProperties():
    try:
        g = request.args.get('g', 0, type=str)
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {?p ?a ?v} }" % (g)
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        triples = []
        properties = []
        annotations = []
        for result in results["results"]["bindings"]:
            properties.append(result['p']['value'])
            annotations.append(result['a']['value'])
            triples.append({'property': result['p']['value'], "annotation": result['a']['value'], "value": result['v']["value"]})
        result = {'properties': list(set(properties)), "annotations": list(set(annotations)), "triples": triples}
        return jsonify(result=result)
    except Exception as e:
        return e


@app.route('/_getAnnotations')
def getAnnotations():
    """ retrieves data for viewing (upon request from JS) """
    try:
        # obtain variables from JS submission
        g = request.args.get('g', 0, type=str)  # triplestore graph namespace
        p = request.args.get('p', 0, type=str)  # property (subject in the subject-predicate-object schema)
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {<%s> ?a ?v} }" % (g, p)
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        triples = []
        annotations = []
        for result in results["results"]["bindings"]:
            annotations.append(result['a']['value'])
            triples.append({'property': p, "annotation": result['a']['value'], "value": result['v']["value"]})
        result = {"annotations": list(set(annotations)), "triples": triples}
        # return results to the JS function
        return jsonify(result=result)
    except Exception as e:
        return e


@app.route('/_setAnnotations')
def setAnnotations():
    """ sets a new value on an existing annotation """
    try:
        # obtain variables from JS submission
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)  # annotation (predicate in the s-p-o schema)
        ov = request.args.get('ov', 0, type=str)  # old value (the value that is being replaced)
        nv = request.args.get('nv', 0, type=str)  # new value (the replacement value)
        u = request.args.get('u', 0, type=str)  # user (for audit)
        # this should be improved by adding a uri test on the ov separate from the new value (unless we agree, some annos must be either uri or lit only)
        uri1 = "PREFIX ual: <http://terms.library.ualberta.ca/> WITH ual:%s DELETE { <%s> <%s> '%s' } INSERT { <%s> <%s> <%s> } WHERE { <%s> <%s> '%s' }" % (g, p, a, ov, p, a, nv, p, a, ov)
        uri2 = "PREFIX ual: <http://terms.library.ualberta.ca/> WITH ual:%s DELETE { <%s> <%s> <%s> } INSERT { <%s> <%s> <%s> } WHERE { <%s> <%s> <%s> }" % (g, p, a, ov, p, a, nv, p, a, ov)
        lit1 = "PREFIX ual: <http://terms.library.ualberta.ca/> WITH ual:%s DELETE { <%s> <%s> <%s> } INSERT { <%s> <%s> '%s' } WHERE { <%s> <%s> <%s> }" % (g, p, a, ov, p, a, nv, p, a, ov)
        lit2 = "PREFIX ual: <http://terms.library.ualberta.ca/> WITH ual:%s DELETE { <%s> <%s> '%s' } INSERT { <%s> <%s> '%s' } WHERE { <%s> <%s> '%s' }" % (g, p, a, ov, p, a, nv, p, a, ov)
        # tests if the new value is a uri or a literal and sets appropriately
        if "http" in ov and nv:
            query = uri2
        elif ("http" in nv) and ("http" not in ov):
            query = uri1
        elif ("http" not in nv) and ("http" not in ov):
            query = lit2
        elif ("http" not in nv) and ("http" in ov):
            query = lit1
        # perform the query
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        auditQ = "prefix dcterms: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix schema: <http://schema.org/> prefix ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:audit { _:blanknode a schema:ReplaceAction ; schema:agent ual:%s ; schema:endTime '%s'^^xsd:dateTime ; dcterms:isPartOf <%s> ; schema:targetCollection <%s> ; schema:object <%s> ; ual:deletion '%s'; ual:insertion '%s' } }" % (u, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), g, p, a, ov, nv)
        sparql.setQuery(auditQ)
        sparql.query()
        # obtains the new value from the graph to ensure the data has changed
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {<%s> <%s> ?v} }" % (g, p, a)
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        # retrieve results
        for result in results["results"]["bindings"]:
            results = result['v']['value']
        # return results to the JS function
        return jsonify(result=[results])
    except Exception as e:
        return e


@app.route('/_delAnnotations')
def delAnnotations():
    """ deletes an annotation from the property """
    try:
        # obtain variables from JS submission
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)
        ov = request.args.get('ov', 0, type=str)
        u = request.args.get('u', 0, type=str)  # user (for audit)
        # tests if the value to be deleted is a uri or a literal and sets appropriately
        if "http" in ov:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, ov)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, ov)
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        auditQ = "prefix dcterms: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix schema: <http://schema.org/> prefix ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:audit { _:blanknode a schema:DeleteAction ; schema:agent ual:%s ; schema:endTime '%s'^^xsd:dateTime ; dcterms:isPartOf <%s> ; schema:targetCollection <%s> ; schema:object <%s> ; ual:deletion '%s'} }" % (u, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), g, p, a, ov)
        sparql.setQuery(auditQ)
        sparql.query()       
        return jsonify(result=None)
    except Exception as e:
        return e


@app.route('/_newAnnotation')
def newAnnotation():
    """ sets an entirely new annotation on the property """
    try:
        # obtain variables from JS submission
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)
        nv = request.args.get('nv', 0, type=str)
        u = request.args.get('u', 0, type=str)  # user (for audit)
        # tests if the value to be added is a uri or a literal and sets appropriately
        if "http" in nv:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, nv)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, nv)
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        auditQ = "prefix dcterms: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix schema: <http://schema.org/> prefix ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:audit { _:blanknode a schema:AddAction ; schema:agent ual:%s ; schema:endTime '%s'^^xsd:dateTime ; dcterms:isPartOf <%s> ; schema:targetCollection <%s> ; schema:object <%s> ; ual:insertion '%s' } }" % (u, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), g, p, a, nv)
        sparql.setQuery(auditQ)
        sparql.query()     
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {<%s> <%s> ?v} }" % (g, p, a)
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            results = [result['v']['value']]
        return jsonify(result=results)

    except Exception as e:
        return e


@app.route('/_view')
def view():
    try:
        query = "prefix dcterms: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix schema: <http://schema.org/> prefix ual: <http://terms.library.ualberta.ca/> select ?date ?type ?graph ?property ?annotation ?insertion ?deletion where {graph ual:audit {?event schema:agent ?user ; rdf:type ?type ; schema:endTime ?date ; dcterms:isPartOf ?graph ; schema:targetCollection ?property ; schema:object ?annotation . OPTIONAL { ?event ual:deletion ?deletion} . OPTIONAL {?event ual:insertion ?insertion } } } ORDER BY desc(?date)"
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        events = []
        for result in results["results"]["bindings"]:
            binding = {#"user": result['userName']['value'], #username isn't working with audit right now. the query needs to be fixed.
                            "date": result['date']['value'],
                            "type": result['type']['value'],
                            "graph": result['graph']["value"],
                            "property": result['property']["value"],
                            "annotation": result['annotation']["value"]
                        }
            if 'insertion' in result:
                binding["insertion"] = result['insertion']["value"]
            if 'deletion' in result:
                binding["deletion"] = result['deletion']["value"]
            events.append(binding)

        # return results to the JS function
        return jsonify(result=events)
    except Exception as e:
        return e        


@app.route('/audit')
def audit():
    try:
        return render_template("audit.html")
    except Exception as e:
        return(e)


@app.route('/')
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True)