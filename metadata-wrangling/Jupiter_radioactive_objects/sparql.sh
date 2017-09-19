#!/bin/bash
i=1 
while read line           
do           
    echo $line  
	 
	 
	curl -G "http://sheff.library.ualberta.ca:9999/blazegraph/namespace/gillingham/sparql" --data-urlencode "query=prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> construct {?r ?p ?value} where {?r ?p ?value {select (SAMPLE(?s) as ?r) where {?s dcterm:rights '$line'^^xsd:string} GROUP by ?value}}" -H 'Accept:application/rdf+xml' > radioactive_dc-rights-$i.xml

((i++))
       
done <rights.txt  





	

