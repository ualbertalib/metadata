package = set(open('data/no_ac_in_transformed.txt').read().split())
migrated = set(open('data/problematic_ac.txt').read().split())

rejected = package.difference(migrated)
notinpackage = migrated.difference(package)

print(rejected)
print(notinpackage)


f_rejected = open('data/results_1.txt','w') 
f_rejected.write(repr(rejected))
f_rejected.close

f_notinpackage = open('data/results_2.txt','w') 
f_notinpackage.write(repr(notinpackage))
f_notinpackage.close