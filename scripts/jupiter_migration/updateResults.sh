curl  -X POST "http://206.167.181.123:9999/blazegraph/namespace/results/sparql" --data-urlencode "update=DELETE {?a ?b ?c} where {?a ?b ?c}" -H 'Accept:text/plain'
FILES=$(find results -type f -name '*.nt')

for i in $FILES
do
	curl -H  'Content-Type: text/turtle' --upload-file $i -X POST 'http://206.167.181.123:9999/blazegraph/namespace/results/sparql'
done