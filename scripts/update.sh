curl  -X POST http://206.167.181.123:9999/blazegraph/namespace/jupiter-latest/sparql --data-urlencode "query=CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }" -H 'Accept:text/plain' > temp.nt
curl -H 'Content-Type: text/plain' --upload-file 'temp.nt' -X POST "http://sheff.library.ualberta.ca:9999/blazegraph/namespace/era-test/sparql"
