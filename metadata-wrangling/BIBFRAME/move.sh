#!/bin/bash
for i in 1 2 3 4 5 6 7 8 9 10 11 
do
echo "starting segment $i"
mkdir -p ~/metadata_work/MARC/Seg-$i
for file in $(ls -p ~/metadata_work/MARC/UADATA-BIBFRAME/| grep -v / | tail -10)
do
mv UADATA-BIBFRAME/$file Seg-$i/
done
echo "Moving files complete"
echo "merging all files"
cat Seg-$i/* > Seg-$i/temp.xml
echo "merging complete"
sed  -i '1i <root>' Seg-$i/temp.xml

(cat Seg-$i/temp.xml ; echo "</root>") > Seg-$i/merged-file.xml

sudo chown mparedes Seg-$i/merged-file.xml
done
