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
   
- configure config.py at [line 44](https://github.com/ualbertalib/metadata/blob/50ba76cbc4bf82500025ecdf849537980d0c39d0/scripts/ia/legacy_Thesis/config.py#L44) to download the desired file type(s) from Internet Archives:
   
- Run IA_thesis.py:

   ```python IA_thesis.py```
   
- Exit the virtual ENV:

   ```deactivate```
