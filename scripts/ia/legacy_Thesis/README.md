# Generating Jupiter campatible packge for U of A Legacy Thesis in Internet Archives

This python package was generated to address issue [#326](https://github.com/ualbertalib/metadata/issues/326).

## How to use
 - make sure that you have python installed. 
 - install pip for your python distribution:
 
   1- securely download get-pip.py.

    ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
    
   2- Inspect get-pip.py for any malevolence. Then run the following:

   ```python get-pip.py```
   
- install virtual environment for python:

   ```python -m pip install --user virtualenv```
   
- create a virtual ENV:

   ```python -m virtualenv env```
   
- activate the virtual ENV:

   ```source env/bin/activate```
   
- install required modules:
   
   ```pip install -r requirements.txt```
   
- configure config.py at [line 44](https://github.com/ualbertalib/metadata/blob/50ba76cbc4bf82500025ecdf849537980d0c39d0/scripts/ia/legacy_Thesis/config.py#L44) to download the desired file type(s) from Internet Archives. Make sure marcxml is included as all the mappings and data extractios are done form the MARC/XML file.
   
- Run IA_thesis.py:

   ```python IA_thesis.py```
   
- Exit the virtual ENV:

   ```deactivate```

## Proccess workflow
Runnig the script will query the ERA triplestore for all thesis with a "unicorn" and will generate list "ERA_IDs.json". Then it will search University of Alberta/Theses and Dissertation collection in Internet Archives and extracts objects that has either ```call_number``` or ```catkey```. Internet Archive ids for items that have either of these will be saved to "IA_IDs.json". 

The two list are then compared and two new lists are generated:

   - All items that are both in ERA and IA -> overlaps.json
 
   - All items that are only in IA (not in ERA) -> IA_only.json
   
All the items in the IA_only list are then downloaded (according to file type(s) in the config.py) into their respective folder.

All the required field (according to [Jupiter Data Dictionary](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_thesis.md) are extracted from the MARC/XML files. Extracted field are (required and not required):

   - title
   - subject
   - graduation date
   - dissertant
   - department
   - institution
   - thesis level
   - degree
   
A UUID is generated randomly (will cross check with all the UUIDs in Jupiter to make sure it is unique) for each item and then all data is saved inot a N-triple file.
