from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
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
    try:
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
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
        return jsonify(result=result)

    except Exception as e:
        return e


@app.route('/_setAnnotations')
def setAnnotations():
    try:
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)
        ov = request.args.get('ov', 0, type=str)
        nv = request.args.get('nv', 0, type=str)
        if "http" in ov:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, ov)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, ov)
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        if "http" in nv:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, nv)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, nv)
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {<%s> <%s> ?v} }" % (g, p, a)
        sparql.setMethod('GET')
        sparql.setQuery(query)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            results = result['v']['value']
        return jsonify(result=[results])

    except Exception as e:
        return e


@app.route('/_delAnnotations')
def delAnnotations():
    try:
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)
        ov = request.args.get('ov', 0, type=str)
        if "http" in ov:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, ov)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> DELETE DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, ov)
        sparql.setMethod('POST')
        sparql.setQuery(query)
        sparql.query()
        return jsonify(result=None)
    except Exception as e:
        return e


@app.route('/_newAnnotation')
def newAnnotation():
    try:
        g = request.args.get('g', 0, type=str)
        p = request.args.get('p', 0, type=str)
        a = request.args.get('a', 0, type=str)
        nv = request.args.get('nv', 0, type=str)
        if "http" in nv:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> <%s> } }" % (g, p, a, nv)
        else:
            query = "PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA {GRAPH ual:%s {<%s> <%s> '%s' } }" % (g, p, a, nv)
        sparql.setMethod('POST')
        sparql.setQuery(query)
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
   

@app.route('/editor', methods=["GET", "POST"])
def editor():
    try:
        return render_template("editor.html")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)