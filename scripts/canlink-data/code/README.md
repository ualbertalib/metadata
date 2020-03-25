#### Python 3+ necessary
#### Can't use the default version of Pymarc since it doesn't work with some encodings - use the modified version from [here](https://github.com/maharshmellow/pymarc)
#### Sandbox contains files that are just for testing purposes - the website does not depend on this
#### The website will run /website/processing/processing.py to process the uploaded records but this is usually not up-to-date with the most recent file /sandbox/rdfgeneration.py which is used for testing - this will eventually get migrated to the website after everything is working
#### Recaptcha on the website is there but currently disabled 
#### The website returns some predefined error and warning messages - the foundation is done but there is a lot more error checking required
#### A DEBUG needs to be turned off and SECRET_KEY needs to be set in the environment variables before making the website live
