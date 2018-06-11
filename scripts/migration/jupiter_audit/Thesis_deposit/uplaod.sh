FILES="/home/danydvd/git/remote/metadata/scripts/migration/jupiter_audit/Thesis_deposit/perms/*"
for f in $FILES
do
	echo $f
	curl -H 'Content-Type: text/turtle' --upload-file $f -X POST "http://206.167.181.124:9999/blazegraph/namespace/Thesis_deposit_Jun112018/sparql"
done