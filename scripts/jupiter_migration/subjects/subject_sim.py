from fuzzywuzzy import fuzz
import re, os, json

ss = []
sd = []
su = []
sv = []
sa = []
for filename in os.listdir(os.getcwd()):
    mod = filename.replace('.py', '')
    if mod == '__pycache__':
        continue
    else:
        subs ="subs"
        subs = getattr(__import__(mod, fromlist=[subs]), subs)
        for i in subs:
            if i['useForm'] in ss:
                continue
            if i in su:
                continue
            else:
                su.append(i)
                ss.append(i["useForm"])
                sd.append(i["mappings"])
for i in ss:
    if i in sv:
        continue
    else:
        temp = i.replace('-- ', '--').replace(' --', '--').replace(' -- ', '--')
        test1 = i.replace('-- ', ' ').replace(' --', ' ').replace(' -- ', ' ').replace('—', ' ').replace('-', ' ').replace('.', '').replace(',', '')
        sg = ['no scoe yet']
        for j in sd:
            test2 = j.replace('-- ', ' ').replace(' --', ' ').replace(' -- ', ' ').replace('—', ' ').replace('-', ' ').replace('.', '').replace(',', '')
            mapp = fuzz.ratio(test1, test2)
            if (len(i) < 10 and int(mapp) < 91) or (len(i) < 20 and int(mapp) < 95) or (len(i) < 30 and int(mapp) < 98) or (len(i) > 29 and int(mapp) < 99):
                continue
            else:
                del sg[0]
                sv.append(j)
                sg.append(j)
        if sg[0] != 'no scoe yet':
            sa.append({'useForm': temp, 'mappings': sg})
with open('subjects1.py', 'a') as out:
    json.dump(sa, out)
print ("done")
