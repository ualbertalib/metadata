import requests
from Passwords import passwords
import re

passwd = passwords['mycombe2'][1]
user = passwords['mycombe2'][0]

permissions = []
noids = ["c4b29b6568", "cp2676w13q", "c7s75dd158", "cg445cd65j", "csn009z339", "cq811kk279", "ck643b168p", "c1g05fc167", "c9s161678m", "c0z708w956", "c0g354f719", "cz029p526w", "cv692t667j", "c2514nk98v", "cnv935337s", "c2227mq36p", "cj96021161", "cdn39x213d", "c6108vb73q", "cw3763725w", "cv979v3603", "cjw827c24h", "cc821gk25h"]
#noids = ["cq811kk232", "c2801pg87d", "c05741s271", "czp38wd19h", "cwd375w50q", "cx346d4691", "cm326m226v", "cs1784m260", "c08612p03c", "ccz30pt306", "c9593tv69q", "c0k225b68b", "ccc08hg14n", "c3j3332734", "c8c97kq85v", "c9w032357w", "cjd472w670", "c6w924c30c", "cwp988k322", "ch128nf27z", "c08612p04p", "cb2773v91w", "crf55z812d", "c8s45q894q", "c3r074v45k", "cg158bh74c", "czk51vh264", "chx11xf66r", "cjs956g321", "cnz806015r", "cth83kz92k", "cnv935325w", "cnc580n159", "cq811kj853", "cpn89d7203", "cw0892b37n", "ct148fh648", "c3j333274f", "c9306sz79k", "cfn106z32t", "cx920fx38z", "c736664672", "cg158bh75p", "chh63sw26r", "cfn106z334", "cj9602111g", "cqv33rx20z", "c7m01bm19c", "c8g84mm75q", "c6h440t039", "c02870w319", "cxg94hq07z", "c7s75dd10q", "c9w0323586", "cq524jp34h", "cqv33rx23w", "cdn39x205r", "cwd375w764", "ck3569484v", "cdr26xx79m", "czc77sq55c", "csj139243n", "c3197xm255", "cw6634386r", "cnv9353266", "cfn106z34f", "c8g84mm761", "c6395w7617", "cth83kz93w", "c1544bp50g", "cdr26xx81d", "cnz8060162", "cjh343s791", "c3f4625955", "ccf95jc053", "c2n49t191k", "cjw827c18g", "cn870zr35z", "c5138jf194", "cvq27zn79v", "cc247ds63q", "cpn89d721d", "cn009w2954", "c00000023v", "crv042t273", "c6m311p83d", "c0r967422h", "c3r074v46w", "cz029p521b", "crx913q27h", "cjw827c19s", "cmk61rh13r", "cn009w296f", "c0g354f69h", "cx633f173k", "c6108vb680", "c7p88ch04j", "c8p58pd48p", "csn009z24b", "cq811kk24c", "c1r66j163q", "cgx41mj44s", "cxw42n840s", "c37720d188", "cfj236229s", "cwd375w78r", "c41687h980", "cjm214p70c", "cgb19f629j", "csj139215f", "cz603qx81t", "c4b29b650d", "c6w924c31p", "cjd472w956", "c4x51hj66s", "c8c97kq612", "cc247ds641", "c0c483j82r", "c79407x674", "cj9602112s", "c5m60qs38m", "cvh53ww26x", "cfn106z362", "cp8418n723", "crv042t648", "cc821gk23w", "c9306sz802", "cz603qx824", "crf55z783d", "crv042t65k", "cpk02cb30c", "cx920fx398", "chx11xf672", "c2227mq314", "cdb78tc554", "cpr76f399q", "cww72bb94c", "c0v838108z", "c37720c940", "cz316q201x", "cw37637238", "cgx41mj453", "c7m01bm20v", "cm039k534c", "cqv33rx246", "cxg94hq088", "ck930bx22n", "cd791sg64c", "cq237hs468", "cfb4949021", "cfj236255c", "ctq57nr38n", "crb68xc44q", "cjw827c21k", "c1544bp51s", "cpc289j57t", "cqz20st01v", "czk51vh28r", "c8p58pd490", "csq87bv06d", "cxg94hp76b", "ctb09j591x", "cgb19f601h", "cxd07gt29q", "cmc87pq80g", "ch128nf288", "c1j92g806c", "cnv935327h", "c9593tv706", "crr171x68c", "cz029p522n", "cqj72p7692", "c6108vb70s", "ckp78gg822", "c8w32r6184", "cqr46r141w", "cx633f174w", "cbc386j67x", "cj3860749h", "c3197xm283", "c3j333240c", "c8049g5641", "cqb98mf96p", "cfx719m96r", "c8g84mm78n", "c3n203z60v", "ck643b1634", "cqr46r1426", "ckd17ct39t", "c4q77fr79q", "cdr26xx82q", "cdn39x207c", "cms35t880c", "c6969z130z", "cb8515n882", "cm900nt83d", "cqz20st025", "c4b29b651q", "ccv43nx35m", "cgt54kn41q", "cc247ds66n", "crf55z787n", "c6395w762j", "c02870w32m", "ccf95jc07q", "chm50ts43h", "c8049g565b", "cc534fp41p", "c8g84mm79z", "cx633f1756", "cfx719m972", "c1r66j1641", "cmc87pq823", "csj139244z", "c9g54xj092", "cq237hs47k", "cf4752h24b", "cp2676w06c", "cc247ds67z", "cg732d947r", "c4x51hj673", "cj9602114d", "cn009w2982", "czs25x904t", "cfx719m98c", "c6h440s702", "c2801pg94r", "crx913q28t", "cdv13zt78f", "c9z903030k", "c1z40kt287", "ckw52j849d", "c1544bp523", "cqz20st03g", "cd217qp98w", "cns0646512", "cd791sg65p", "c9019s3033", "cr494vk58c", "ckw52j850w", "ccv43nx36x", "cj6731437r", "cz890rt695", "c1g05fc09w", "cdn39x208p", "cmp48sd31d", "c3t945r23t", "c8g84mm80f", "ccv43nx38j", "cjs956g33b", "c0z708w91z", "cbz60cw72w", "cqb98mf989", "ctm70mv692", "ck930bx543", "cxd07gt31h", "cst74cq99q", "cb5644s140", "c3484zh13d", "cng451j055", "czk51vh31v"]
headers = {'Content-type': 'text/xml',}

for n, i in enumerate(noids):
	print ("processing noid number " + str(n))
	solr_q = "http://tottenham.library.ualberta.ca:8080/solr/hydranorth_shard1_replica3/select?q=accessTo_ssim:%s&wt=json&indent=true" %(i)
	solr_response = requests.get(solr_q).json()
	for item in solr_response['response']['docs']:
		if item['id'] not in permissions:
			permissions.append(item['id'])
	for perm_id in permissions:
		perm_q = "http://mycombe2.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" %(perm_id[0:2], perm_id[2:4], perm_id[4:6], perm_id[6:8], perm_id)
		perm_response = requests.get(perm_q, headers=headers, auth=(user, passwd)).text
		with open('Thesis_deposit/perms1/' + perm_id + '.nt', 'w') as perm_obj:
			perm_obj.write(perm_response)
			perm_obj.close()
	object_q = "http://mycombe2.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" %(i[0:2], i[2:4], i[4:6], i[6:8], i)
	response = requests.get(object_q, headers=headers, auth=(user, passwd)).text
	with open('Thesis_deposit/obj1/' + i + '.nt', "w") as output:
		output.write(response)
		output.close()
	with open('Thesis_deposit/obj1/' + i + '.nt', "r") as inpu:
		for line in inpu:
			if re.search('hasEmbargo', line):
				embargo_q = line.replace('hydraacl:hasEmbargo <', '').replace('> ;', '').replace('\n', '').lstrip()
				id = embargo_q.split('/')[-1]
				embargo_response = requests.get(embargo_q, headers=headers, auth=(user, passwd)).text
				with open('Thesis_deposit/embargo1/' + id + '.nt', 'w') as embargo_obj:
					embargo_obj.write(embargo_response)
					embargo_obj.close()
	'''files = {'upload_file': open('t/' + i + '.nt','rb')}
	print (files)
	upload = requests.post('http://206.167.181.124:9999/blazegraph/namespace/test/sparql', files=files)
	print(upload.status_code, upload.reason)'''



