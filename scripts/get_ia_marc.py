#!/usr/bin/python

import internetarchive

from internetarchive import get_session
c = {'s3': {'access': 'hxkfJQqTVuut2W1T', 'secret': 'oliIhQ0uXYpnjYWd'}}
s = get_session(config=c)
s.access_key
'hxkfJQqTVuut2W1T'

search = internetarchive.search_items('collection:albertagovernmentpublications')

for result in search:
    itemid = result['identifier']
    item = internetarchive.get_item(itemid)
    marc = item.get_file(itemid + '_marc.xml')
    marc.download()
    print "Downloading " + itemid + " ..."
