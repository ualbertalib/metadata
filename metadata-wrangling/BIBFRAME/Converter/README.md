# UAL BIBFRAME enrichment processor 

This is program developed in python for Conversion of marc data into BIBFRAME and Reconciliation and Enrichment of BIBFRAME data.

## How to use
 - make sure that you have python installed. 
 - install pip for your python distribution:
 
   1- securely download get-pip.py.

    ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
    
   2- Inspect get-pip.py for any malevolence. Then run the following:

   ```python get-pip.py```
   
- install virtual environment for python:

   ```python -m pip install --user virtualenv```
   
- create a virtualENV:

   ```python -m virtualenv env```
   
- activate the virtualENV:

   ```source env/bin/activate```
   
- install required modules:
   
   ```pip install -r requirements.txt```
   
- Once the process is finished, exit the virtualENV:

   ```deactivate```
## APIs

This process searches the following APIs to enrich names with URIs:

- VIAF Auto Suggest: http://viaf.org/viaf/AutoSuggest?query=QUERY
- VIAF personal names: https://viaf.org/viaf/search?query=local.personalNames+all+QUERY
- VIAF corporate names: https://viaf.org/viaf/search?query=local.corporateNames+all+QUERY
- Library of Congress Suggest: http://id.loc.gov"/authorities/names/suggest/?q=QUERY
- Library of Congress Did you mean: http://id.loc.gov"authorities/names/didyoumean/?label=QUERY

**NOTE:** VIAF Personal and Corporate APIs include reference to LC numbers as well. These numbers are as LC_ids if both Library of Congress APIs fails to provide a match.


## Process workflow
- Make sure that a folder named "source" and the sub-folders "marc" and "BIBFRAME" exists in the root directory.
- If your source files are MARC (.mrc) files, paste them into the "marc" folder.
- If your source files are BIBFRAME (.xml) files, paste them into the "BIBFRAME" folder.
- Run enrich.py

   ```python enrich.py```
  
The process will look for all .mrc files in the source/marc folder and will convert them to MARC/XML format saving them as individual records (records in marc data). All the records associated with a certain .mrc file (which will be referred as master_file) will be saved into a sub-folder named as: "master_file + timestamp" in the "MARC/XML" folder.

The process then starts working on the MARC/XML files and convert them into BIBFRAME using the Library of Congress Marc to BIBFRAME converter. The individual BIBFRAME files will be saved in a sub-folder named "master_file + timestamp" in the BIBFRAME folder. 

The process will also searches for BIBFRAME files (.xml format) in the source/BIBFRAME folder

For better performance, all individual BIBFRAMEs associated with master_file are merged into a single BIBFRAME file. From this point onward the enrichment process takes place. All names (bf:Agent in BIBFRAME) and titles (bf:title in BIBFRAME) are extracted from the merged-file using an xslt script. The process retrieve URIs from the specifics APIs and write them back into the BIBFRAM file.
