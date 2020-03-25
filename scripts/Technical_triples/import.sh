for file in *.ttl
	do
		echo "uploading " $file
		curl -X POST -H "Content-Type:text/turtle" -u "admin:4Metadata!" -T $file http://206.167.181.124:7200/repositories/fedora_24022020/statements
	done