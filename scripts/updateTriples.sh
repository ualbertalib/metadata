FILES="/home/zschoenb/Documents/nt/*"
for f in $FILES
do
	echo $f
	curl -H 'Content-Type: text/turtle' --upload-file $f -X POST "http://206.167.181.123:9999/blazegraph/namespace/jupiter-inference/sparql"
done
