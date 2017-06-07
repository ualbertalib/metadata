#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
b=${line// /}
a=`expr index "$line" ,`
file1=${line//./-}
file2=${file1//,/-}
file3=${file2// /}
echo $file3
	touch $file3.xml
echo "creating $line"
  curl -X GET --header "Accept:application/vnd.orcid+xml" 'https://pub.orcid.org/v2.0/search?q='"$b"'' > $file3.xml

done < "$1"

