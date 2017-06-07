#!/usr/bin/python

import time 
import internetarchive

#without s3
from internetarchive import configure
configure('username', 'passwd')

#s3 for Danoosh
from internetarchive import get_session
c = {'s3': {'access': 'C9khuFEwAKAj5Y5X', 'secret': '8s5NsWQzx1wTKfAd'}}
s = get_session(config=c)
s.access_key
'C9khuFEwAKAj5Y5X'

search = internetarchive.search_items('collection:albertagovernmentpublications')

for result in search:
    itemid = result['identifier']
    item = internetarchive.get_item(itemid)
    marc = item.get_file(itemid + '_marc.xml')
    marc.download()
    print "Downloading " + itemid + " ..."
    time.sleep(0)
