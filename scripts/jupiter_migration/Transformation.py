from config import vocabs

"""TRANSFORMATION functions for handling data passed over by the data object. Takes a triple, detects what kind of action needs to be taken based on the predicate, sends it to the appropriate function for transformations, then returns it back to the data handler to be saved."""

class Transformation():

    def __init__(self):
        self.output = []

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
            triple['object']['value'] = "http://terms.library.ualberta.ca/private"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def available(self, triple, objectType):
        self.output.append(triple)
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
                    'value': "http://terms.library.ualberta.ca/public",
                    'type': 'uri'
                }
            }
        )
        return self.output
