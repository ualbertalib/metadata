#!/bin/bash
for file in ./*.txt;
do
	sudo mkdir "${file%.*}"   
        sudo chown mparedes "${file%.*}"   
	index=0    
	head -10 $file |
	while read line;
	
	do
		(( index++ ))
		echo $index
		echo "creating" "$index"_"$line"
		curl -X GET --header "Accept:application/vnd.orcid+xml" 'https://pub.orcid.org/v2.0/'"$line"'/record' > "$index"_"$line".xml
		echo "own"
		sudo chown mparedes "$index"_"$line".xml
		echo "mv"
		mv "$index"_"$line".xml "${file%.*}"
		echo "file done"
	done
mv "$file" "${file%.*}"
done
