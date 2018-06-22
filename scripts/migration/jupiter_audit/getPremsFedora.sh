#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"

	name="$(cut -d'/' -f11 <<<"$line")"
	echo $name
<<<<<<< HEAD
	curl -u "fedoraAdmin:HN4di2015" -H "Content-type:application/xml" -X GET $line >> "CPermissions.nt"
=======
	curl -u "username:password" -H "Content-type:application/xml" -X GET $line >> "CPermissions.nt"
>>>>>>> master
done < "cperms-uri.txt"