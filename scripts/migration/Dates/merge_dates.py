from config import dates
from ERA_dates import dates_m
from final_extract import date
from final_extract_No_dcterm import d

subjects = []
date = []
for subject in dates:
	sub = subject['subject']
	subjects.append(sub)
print (len(subjects))
print (len(dates_m))
'''for subs in dates_m:
    s = subs['subject']
    if s in subjects:
    	print (s)
    	continue
    else:
        dates.append(subs)
print (len(dates))

print (len(date))
for subs in date:
    s = subs['subject']
    if s in subjects:
    	print (s)
    	continue
    else:
        dates.append(subs)
print (len(dates))'''

print (len(d))
for subs in d:
    s = subs['subject']
    if s in subjects:
    	continue
    else:
        date.append(subs)
print (len(dates))

with open("dates_no_created.py", "a") as output:
    output.write("dates = [")
    for subs in date:
        output.write(str(subs))
        output.write(",")
        output.write("\n")
    output.write("]")


