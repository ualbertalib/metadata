import requests
import json
from time import sleep

def main():
	parseHandles(SOLR())

def SOLR():
	access = []
	id = []
	for i in range(186):
		i = i * 1000
		print(i)
		r = requests.get('http://tottenham.library.ualberta.ca:8080/solr/hydranorth_shard1_replica1/select', params={'q': '*:*', 'fq': '!active_fedora_model_ssi:Batch', 'fl': 'accessTo_ssim, id', "start": i, "rows": '999', 'wt': 'json', 'indent': 'true'})
		for handle in r.json()["response"]["docs"]:
			if 'accessTo_ssim' in handle:
				access.append(handle['accessTo_ssim'][0])
			if 'id' in handle:
				id.append(handle['id'][0])
	return (access, id)


def parseHandles(handles):
	access = list(set(handles[0]))
	id = list(set(handles[1]))
	with open('resources.txt', 'w') as f:
		for h in access:
			if "-" not in h:
				f.write("%s\n" % "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" % (h[0:2], h[2:4], h[4:6], h[6:8], h))
		for h in id:
			f.write("%s\n" % "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" % (h[0:2], h[2:4], h[4:6], h[6:8], h))


if __name__ == "__main__":
	main()
