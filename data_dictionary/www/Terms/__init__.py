from flask import Flask, render_template, request, jsonify
from wtforms import Form, TextField, BooleanField, validators
from SPARQLWrapper import SPARQLWrapper, JSON
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



@app.route('/_getA')
def getAnnotations():
    try:
        graph = request.args.get('profile', 0, type=str)
        p = request.args.get('property', 0, type=str)
        sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select ?a where {GRAPH ual:%s {?a ?b ?c} }" % (graph)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
             output.append(result['a']["value"])
        return jsonify(result=list(set(output)))

    except Exception as e:
        return e


@app.route('/_getP')
def getProperties():
    try:
        graph = request.args.get('graph', 0, type=str)
        sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
        query = "PREFIX ual: <http://terms.library.ualberta.ca/> select ?a where {GRAPH ual:%s {?a ?b ?c} }" % (graph)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            output.append(result['a']["value"])
        return jsonify(result=list(set(output)))

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