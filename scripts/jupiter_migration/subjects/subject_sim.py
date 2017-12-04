from fuzzywuzzy import fuzz
import re, os, json

#os.chdir("subjects")
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
for i in sd:
    if i in ss:
        continue
    else:
        ss.append(i)
#print (ss)
for i in ss:
    if i.replace(',', '').replace('.', '') in sv:
        continue
    else:
        temp = i.replace('-- ', '--').replace(' --', '--').replace(' -- ', '--').replace('.', '').replace(',', '')
        test1 = i.replace('-- ', ' ').replace(' --', ' ').replace(' -- ', ' ').replace('—', ' ').replace('-', ' ').replace('.', '').replace(',', '')
        sg = []
        for j in ss:
            if j in sv:
                continue
            else:
                if i[-1] == "s" and i[0:-1] == j:
                    #print (i, j)
                    sv.append(i)
                    sv.append(j)
                    sg.append(j)
                    sa.append({'useForm': i, 'mappings': sg})
            
for i in ss:
    if i.replace(',', '').replace('.', '') in sv:
        #print ("first:" + i)
        continue
    else:
        #print ("second: " + i)
        temp = i.replace('-- ', '--').replace(' --', '--').replace(' -- ', '--').replace('.', '').replace(',', '')
        test1 = i.replace('-- ', ' ').replace(' --', ' ').replace(' -- ', ' ').replace('—', ' ').replace('-', ' ').replace('.', '').replace(',', '')
        sg = []
        for j in ss:
            if j in sv:
                continue
            else:
                test2 = j.replace('-- ', ' ').replace(' --', ' ').replace(' -- ', ' ').replace('—', ' ').replace('-', ' ').replace('.', '').replace(',', '')
                mapp = fuzz.ratio(test1, test2)
                #print (i, j, mapp)
                if len(i) < 10 and int(mapp) < 91:
                    continue
                elif ((len(i) > 9 and len(i) < 20) and int(mapp) < 93):
                    continue
                elif ((len(i) > 19 and len(i) < 30) and int(mapp) < 98):
                    continue
                elif (len(i) >29 and int(mapp) < 99):
                    continue
                elif i == j:
                    continue
                else:
                    sv.append(i)
                    sv.append(j)
                    if j not in sg:
                        sg.append(j)
        sa.append({'useForm': temp, 'mappings': sg})
#print (sa)
with open('subjects1.py', 'a') as out:
    out.write('subjects = [')
    for i in sa:
        if i['useForm'] != i['mappings']:
            le = len(i['mappings'])
            if le != 0:
                if "—" in i['useForm']:
                    for z in i['mappings']:
                        if "--" in z:
                            temp_map = z.replace('-- ', '--').replace(' --', '--').replace(' -- ', '--')
                            out.write('{"useForm":' + '"' + temp_map + '",' + '\n')
                            out.write('"mappings": [')
                            out.write('"' + i['useForm'] + '", ')
                            for l, j in enumerate(i['mappings']):
                                if l < (le-1):
                                    out.write(', "' + j + '",')
                                else:
                                    out.write('"' + j + '"')
                            out.write(']},' + '\n') 
                else:
                    out.write('{"useForm":' + '"' + i['useForm'] + '",' + '\n')
                    out.write('"mappings": [')
                    for l, w in enumerate(i['mappings']):
                        if l < (le-1):
                            out.write('"' + w + '",')
                        else:
                            out.write('"' + w + '"')
                    out.write(']},' + '\n')
             #   json.dump(sa, out)
print ("done")
