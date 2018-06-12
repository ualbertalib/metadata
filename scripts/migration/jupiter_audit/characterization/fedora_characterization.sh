#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"

	name="$(cut -d'/' -f11 <<<"$line")"
	echo $name
	curl -u "username:password" -H "Content-type:application/xml" -X GET $line > "xmls"/$name.xml
done < "noids.txt"