import re
from config import subjects, vocabs, owners
from datetime import datetime, date
from Classes.DateFinder import DateFinder

"""TRANSFORMATION functions for handling data passed over by the data object. Takes a triple, detects what kind of action needs to be taken based on the predicate, sends it to the appropriate function for transformations, then returns it back to the data handler to be saved."""


class Transform():

    def __init__(self):
        self.output = []

    def subject(self, triple, objectType):
        """map subjects"""
        for subject in subjects:
            if (triple['object']['value'] in subject['mappings']):
                triple = {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': triple['predicate']['value'],
                            'type': 'uri'
                        },
                        'object': {
                            'value': subject['useForm'],
                            'type': 'literal'
                        }
                    }
        """strip whitespaces/periods off front and back & capitalize first letter"""
        triple['object']['value'] = triple['object']['value'].strip().strip('.').replace('-- ', '--').replace(' --', '--').replace(' -- ', '--')
        triple['object']['value'] = triple['object']['value'][0].upper() + triple['object']['value'][1:]
        self.output.append(triple)
        return self.output

    def language(self, triple, objectType):
        # normalize values and convert to URI (consult the "vocabs" variable from the config file (this folder))
        for vocab in vocabs["language"]:
            # mint a new triple with the mapped type
            if triple['object']['value'] in vocab["mapping"]:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': triple['predicate']['value'],
                            'type': 'uri'
                        },
                        'object': {
                            'value': vocab["uri"],
                            'type': 'uri'
                        }
                    }
                )

            # "other" labels can be changed to specific languages manually.

        return self.output

    def rights(self, triple, objectType):
        # several different license values need to be coerced into one common value, this needs to be confirmed with leah before it is written
        self.output.append(triple)
        return self.output

    def aclvisibilityAfterEmbargo(self, triple, objectType):
        if ("open" in triple['object']['value']) or ("open access" in triple['object']['value']):
            triple['object']['value'] = "http://terms.library.ualberta.ca/public"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        elif "university_of_alberta" in triple['object']['value']:
            triple['object']['value'] = "http://terms.library.ualberta.ca/authenticated"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def institution(self, triple, objectType):
        self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': triple['predicate']['value'],
                    'type': 'uri'
                },
                'object': {
                    'value': 'http://id.loc.gov/authorities/names/n79058482',
                    'type': 'uri'
                }
            }
        )
        return self.output

    def license(self, triple, objectType):
        # convert licenses from text to URI (use vocabs variable, some coersion will be necessary)
        if "I am required to use/link to a publisher's license" in triple['object']['value']:
            return None
        else:
            for vocab in vocabs["license"]:
                if triple['object']['value'] in vocab["mapping"]:
                    self.output.append(
                        {
                            'subject': {
                                'value': triple['subject']['value'],
                                'type': 'uri'
                            },
                            'predicate': {
                                'value': triple['predicate']['value'],
                                'type': 'uri'
                            },
                            'object': {
                                'value': vocab["uri"],
                                'type': 'uri'
                            }
                        }
                    )
            if len(self.output) > 0:
                return self.output
            else:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': "http://purl.org/dc/elements/1.1/rights",
                            'type': 'uri'
                        },
                        'object': {
                            'value': triple['object']['value'],
                            'type': 'literal'
                        }
                    }
                )
                return self.output

    def type(self, triple, objectType):
        if objectType == 'generic':
            for vocab in vocabs["type"]:
                # mint a new triple with the mapped type
                if triple['object']['value'] in vocab["mapping"]:
                    self.output.append(
                        {
                            'subject': {
                                'value': triple['subject']['value'],
                                'type': 'uri'
                            },
                            'predicate': {
                                'value': triple['predicate']['value'],
                                'type': 'uri'
                            },
                            'object': {
                                'value': vocab["uri"],
                                'type': 'uri'
                            }
                        }
                    )
            else:
                pass
        elif (objectType == 'community') or (objectType == 'collection'):
            self.output.append(triple)
        return self.output

    def modelsmemberOf(self, triple, objectType):
        if "http" not in triple['object']['value']:
            value = triple['object']['value']
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/{}/{}/{}/{}/{}".format(value[0:2], value[2:4], value[4:6], value[6:8], value)
            triple['object']['type'] = 'uri'
        self.output.append(triple)
        return self.output

    def modelshasMember(self, triple, objectType):
        if "http" not in triple['object']['value']:
            value = triple['object']['value']
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/{}/{}/{}/{}/{}".format(value[0:2], value[2:4], value[4:6], value[6:8], value)
            triple['object']['type'] = 'uri'
        self.output.append(triple)
        return self.output

    def accessRights(self, triple, objectType):
        if "http://projecthydra.org/ns/auth/group#public" in triple['object']['value']:
            triple['object']['value'] = "http://terms.library.ualberta.ca/public"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        elif ("http://projecthydra.org/ns/auth/group#university_of_alberta" in triple['object']['value']) or ("http://projecthydra.org/ns/auth/group#registered" in triple['object']['value']):
            triple['object']['value'] = "http://terms.library.ualberta.ca/authenticated"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        else:
            triple['object']['value'] = "http://terms.library.ualberta.ca/draft"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def available(self, triple, objectType):
        if datetime.strptime(re.sub(r"[T].+$", "", triple['object']['value']), "%Y-%m-%d").date() > date.today():
            self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': "http://purl.org/dc/terms/accessRights",
                    'type': 'uri'
                },
                'object': {
                    'value': "http://terms.library.ualberta.ca/embargo",
                    'type': 'uri'
                }
            }
            )
        self.output.append(triple)
        return self.output

    def createdDate(self, d, triple, objectType):
        tempTriple = {
            'subject': {
                'value': triple['subject']['value'],
                'type': 'uri'
            },
            'predicate': {
                'value': triple['predicate']['value'],
                'type': 'uri'
            },
            'object': {
                'value': d["object"][0],
                'type': 'date'
            }
        }
        self.output.append(tempTriple)
        Transformation.sortYear(self, tempTriple, objectType)
        return self.output

    def gradDate(self, d, triple, objectType):
        tempTriple = {
            'subject': {
                'value': triple['subject']['value'],
                'type': 'uri'
            },
            'predicate': {
                'value': triple['predicate']['value'],
                'type': 'uri'
            },
            'object': {
                'value': d["object"][0],
                'type': 'date'
            }
        }
        self.output.append(tempTriple)
        Transformation.sortYear(self, tempTriple, objectType)
        return self.output

    def sortYear(self, triple, objectType):
        self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': triple['predicate']['value'],
                    'type': 'uri'
                },
                'object': {
                    'value': triple['object']['value'],
                    'type': 'date'
                }
            }
        )
        if isinstance(triple['object']['value'], list):
            text = triple['object']['value'][0].replace(';', ' ').replace(':', ' ').replace('_', ' ').replace('-', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ')
        else:
            text = triple['object']['value'].replace(';', ' ').replace(':', ' ').replace('_', ' ').replace('-', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ')
        tokens = word_tokenize(text)
        for n,i in enumerate(tokens):
            if i == "," :
                del tokens[n]
            if i == ")" :
                del tokens[n]
            if i == "(" :
                del tokens[n]
        years = DateFinder(tokens)
        trans = years.getyear()
        if trans != None:
            for i in trans:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': 'http://terms.library.ualberta.ca/date/sortyear',
                            'type': 'uri'
                        },
                        'object': {
                            'value': i["year"],
                            'type': 'date'
                        }
                    }
                )
            return self.output

    def owner(self, triple, objectType):
        triple['object']['value'] = triple['subject']['value'].strip("http://projecthydra.org/ns/auth/person#")
        triple['object']['value'] = triple['subject']['value'].strip("http://projecthydra.org/ns/auth/group#")
        if triple['object']['value'] in owners:
            triple['object']['value'] = "eraadmi@ualberta.ca"
        self.output.append(triple)
        return self.output
