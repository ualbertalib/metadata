#!/bin/sh
#
#
mkdir -p website/processing/files
mkdir website/processing/errors
mkdir website/processing/tmp
cp data/*.pickle website/processing/files/.
chown www-data.www-data -R /home/danydvd/CanLink/code/website/processing/
