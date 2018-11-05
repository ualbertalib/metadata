#!/bin/bash

# curl -vv --user $pass --limit-rate 45K sleep 1s --request DELETE --config data/derivative_urls.txt 

curl -vv --user $pass --limit-rate 45K sleep 1s --request DELETE --config data/phantom_masterfile-urls.txt 

curl -vv --user $pass -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:21435.xml' http://129.128.216.228:8080/fedora/objects/avalon:21435/datastreams/sectionsMetadata?logMessage=Delete%20reference%20to%20empty%20MasterFile
curl -vv --user $pass -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:38370.xml' http://129.128.216.228:8080/fedora/objects/avalon:38370/datastreams/sectionsMetadata?logMessage=Delete%20reference%20to%20empty%20MasterFile
curl -vv --user $pass -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:38594.xml' http://129.128.216.228:8080/fedora/objects/avalon:38594/datastreams/sectionsMetadata?logMessage=Delete%20reference%20to%20empty%20MasterFile
curl -vv --user $pass -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:39253.xml' http://129.128.216.228:8080/fedora/objects/avalon:39253/datastreams/sectionsMetadata?logMessage=Delete%20reference%20to%20empty%20MasterFile
curl -vv --user $pass -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:19900.xml' http://129.128.216.228:8080/fedora/objects/avalon:19900/datastreams/sectionsMetadata?logMessage=Delete%20reference%20to%20empty%20MasterFile