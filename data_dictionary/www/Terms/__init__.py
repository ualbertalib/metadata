from flask import Flask, render_template, request, jsonify
from wtforms import Form, TextField, BooleanField, validators
from SPARQLWrapper import SPARQLWrapper, JSON
import json
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])

def run():
    try:
        form = editProperties(request.form)
        if request.method == "POST" and form.validate():
            newProperty = form.newProperty.data
        return render_template("index.html")
    except Exception as e:
        return str(e)


class editProperties(Form):
    newProperty = TextField('newProperty', [validators.Length(max=20)])
    implemented = BooleanField('implemented', [validators.Required()])


@app.route('/_getProperties')
def _getProperties():
    try:
        g = request.args.get('g', 0, type=str)
        sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {?p ?a ?v} }" % (g)
        sparql.setReturnFormat(JSON)
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
        sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select distinct ?p ?a ?v where {GRAPH ual:%s {<%s> ?a ?v} }" % (g, p)
        sparql.setReturnFormat(JSON)
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


@app.route('/editor', methods=["GET", "POST"])
def editor():    
    try:
        return render_template("editor.html")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)