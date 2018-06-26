import xml.etree.ElementTree as ET
import glob

pids = []
files = glob.glob('query_results/[0-9]*.xml')
ns = {'ns0':'http://www.fedora.info/definitions/1/0/types/'}
file = open('avalon_pids.txt', 'w')

def main():
	for f in files:
		with open(f, 'r', encoding='utf-8') as content:
			tree = ET.parse(content)
			root = tree.getroot()
			# print(root)

			for fpid in root.findall('.//ns0:pid', ns):
				pids.append(fpid.text)
				file.write('%s\n' % fpid.text)

if __name__ == "__main__": main()

print(pids)