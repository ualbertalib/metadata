# BIBFRAME enrichment process

This is the process for converting MARC files to BIBFRAME and enriching them with URIs form [LC](http://id.loc.gov/) and [VIAF](http://viaf.org/) APIs.

The process is as follows:

1. Use XMLHandler class in pymarc to convert .mrc to .xml (use $245a as the filename, e.g. titile123.xml)
2. Run all the .xml files through the [Library of Congress MARC to BIBFRAME convertor](https://github.com/ualbertalib/metadata/blob/master/stylesheets/marc2bibframe2-master/xsl/marc2bibframe2.xsl) to get the BIBFRAME/XML files.
3. Use unix cat to merge the BIBFRAME.xml files together (one merged-file.xml file for each collection). Since some collections might have a large number of files, use [move.sh](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/BIBFRAME/move.sh) to speed-up the process. 
4. Apply stylesheet [names.xsl](https://github.com/ualbertalib/metadata/blob/master/stylesheets/BIBFRAME/names.xsl) and [Bibframe-subjects.xsl](https://github.com/ualbertalib/metadata/blob/master/stylesheets/BIBFRAME/Bibframe-subjects.xsl) to extract all names and subjects, respectively, in form of a .tsv. The tsv also includes the example.org URIs from the rdf:about attribute of the name (bf:Agent) or the subject (bf:Topic) to be used as a unique key for ingesting the URIs later on.
5. Start an OpenRefine project for each tsv and apply the appropriate .json OpenRefine process

    **NOTE:** For reconciling against LC API, run [reconcile.py](https://github.com/cmh2166/lc-reconcile/blob/master/reconcile.py) at 0.0.0.0:5000
    
6. Export the OpenRefine completed project as a tsv.
7. Apply stylesheet [Bibframe_LC_URI](https://github.com/ualbertalib/metadata/blob/master/stylesheets/BIBFRAME/Bibframe_LC_URI.xsl) or [Bibframe_VIAF_URI](https://github.com/ualbertalib/metadata/blob/master/stylesheets/BIBFRAME/Bibframe_VIAF_URI.xsl) to the exported tsv (form [LC-OR-process.json](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/BIBFRAME/UADATA-BIBFRAME-Segmented/names/LC/LC-OR-process.json) or [VIAF-OR-process.json](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/BIBFRAME/UADATA-BIBFRAME-Segmented/names/VIAF/VIAF-OR-process.json) and the merged-file (form step 3) to replace the example.org URI in the rdf:about attribute of the bf:Agent with LC or VIAF URIs.
8. Apply stylesheet [Bibframe_Subjects_ingest](https://github.com/ualbertalib/metadata/blob/master/stylesheets/BIBFRAME/Bibframe_Subjects_ingest.xsl) to the exported tsv (form [LSCH-OR-process.json](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/BIBFRAME/UADATA-BIBFRAME-Segmented/subjects/LCSH-OR-process.json)) and the output file from the previous step to replace the example.org URI in the rdf:about attribute of the bf:Topic with LCSH URIs. 


![Alt text](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/BIBFRAME/Bibframe_enrichment_process.JPG "Optional title")
