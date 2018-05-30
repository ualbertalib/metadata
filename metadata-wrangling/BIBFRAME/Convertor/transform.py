import rdflib

g = rdflib.Graph()
result = g.parse("UADATA-Seg-2-enhanced-test.xml")

print("graph has %s statements." % len(g))

s = g.serialize(destination='test.nt', format='nt')