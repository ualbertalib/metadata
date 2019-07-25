#!/usr/bin/python

import time 
import internetarchive

#without s3
from internetarchive import configure
configure('danoosh@ualberta.ca', 'dane1365')

#s3 for Danoosh
from internetarchive import get_session, modify_metadata
c = {'s3': {'access': 'C9khuFEwAKAj5Y5X', 'secret': '8s5NsWQzx1wTKfAd'}}
s = get_session(config=c)
s.access_key
'C9khuFEwAKAj5Y5X'

'''search = internetarchive.search_items('collection:albertagovernmentpublications')

for result in search:
    itemid = result['identifier']
    item = internetarchive.get_item(itemid)
    marc = item.get_file(itemid + '_marc.xml')
    print (marc)'''

r = modify_metadata('vulcan_test_pdf_2', metadata=dict(title='Vulcan Advocate test 2', language='English', description='Page 1 \n - VULCAN--TEN YEARS AGO: Interesting Facts Gleaned from Advocate Files of Nov. 10, 1920 by the “Cub Reporter” <a href="https://archive.org/stream/vulcan_test_pdf_2/VA_19301113#mode/2up">link</a>, \n - KIRKCALDY NEWS, \n - ANOTHER CONCERT BY VULCAN PRIZE BAND, \n - HOCKEY NOTES, \n - ENSIGN NEWS, \n - Vulcan School Report for Month of October, \n - CURLERS PREPARE FOR FORTHCOMING SEASON, \n - MILO NEWS, \n - MALE CHORUS FORMED AT MEETING TUESDAY, \n - MORE NEXT WEEK, \n - RICHMOND HILL NEWS, \n - UNION JACK NEWS, \n - BERRYWATER U.F.W.A. PRESENTS FINE SHOW, \n - LOCAL ITEMS, \n\n Page 2 \n - GOOD CUSTOM GONE <a href="https://archive.org/stream/vulcan_test_pdf_2/VA_19301113#mode/n1/2up">link</a>, \n - NOTES & COMMENTS, \n - BUY NOW, \n - LETTER TO WOMEN, \n - ITEMS OF INTEREST, \n - GAME DEPLETION, \n - MASS PRODUCTION, \n - STORIES RETOLD, \n - WORDS WELL SPOKEN, \n - BY ANY OTHER NAME, \n\n Page 3 \n - IS JAZZ DOOMED?, \n - New Queen Salutes Former Sovereign, \n - THE JUNK PILE, \n - NEW SOUTH TURNER: New Project in South Turner Argues Confidence in Production, \n - MEIGHEN TO RETURN: Toronto Accorded Arthur Meighen Tremendous Reception, \n - SHOW BIG INCREASE: Oil Deliveries to Regal Refineries Show Big Increase, \n - INTERESTING NEWS, \n\n Page 4 \n - YPRES IN 1930: Lethbridge Visitors Describe Impressions of Battlefields, \n - MASTER FARMERS, \n - ROWELL OPTIMIST: Canada Promises to be Future Granary of World, \n - THE FAMILY TREES, \n - WE’RE NOT AS THEY, \n - MUST BALANCE: An Adjustment Must be Made Before Conditions Improve, \n - NEW POLICY LIKELY: Minister of Agriculture Will Revise Policy of His Department, \n - MAIL CONTRACT, \n - EVERY LITTLE HELPS'))
