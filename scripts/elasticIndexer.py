from elasticsearch import helpers, Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
from dateutil import parser as parser

indexSettings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "resource": {
            "properties": {
                "subject": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "resourceType": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "doi": {
                    "type": "text",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "contributor": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "creator": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "spatial": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "temporal": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "date"
                        }
                    }
                },
                "dateCreated": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "date",
                            "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss+SS:SS||yyyy-MM-dd'T'HH:mm:ss'Z'"
                        }
                    }
                },
                "dissertant": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "dateAccepted": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "date",
                            "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss+SS:SS||yyyy-MM-dd'T'HH:mm:ss'Z'"
                        }
                    }
                },
                "department": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "degree": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "specialization": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "level": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "supervisor": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "committee": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                },
                "collection": {
                    "type": "keyword",
                    "fields": {
                        "label": {
                            "type": "text"
                        }
                    }
                }
            }
        }
    }
}


def main():
    sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/ERA/sparql")
    query = """prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {OPTIONAL {?resource <http://purl.org/dc/terms/type> ?resourceType } . OPTIONAL {?resource <http://purl.org/dc/terms/identifier> ?doi } . OPTIONAL {?resource <http://purl.org/dc/terms/title> ?title } . OPTIONAL {?resource <http://purl.org/dc/terms/contributor> ?contributor } . OPTIONAL {?resource <http://purl.org/dc/terms/creator> ?creator } . OPTIONAL {?resource <http://purl.org/dc/terms/spatial> ?spatial } . OPTIONAL {?resource <http://purl.org/dc/terms/temporal> ?temporal } . OPTIONAL {?resource <http://purl.org/dc/terms/subject> ?subject } . OPTIONAL {?resource <http://purl.org/dc/terms/created> ?dateCreated } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/dis> ?dissertant } . OPTIONAL {?resource <http://purl.org/dc/terms/dateAccepted> ?dateAccepted } . OPTIONAL {?resource <http://vivoweb.org/ontology/core#AcademicDepartment> ?department } . OPTIONAL {?resource <http://purl.org/ontology/bibo/ThesisDegree> ?degree } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/specialization> ?specialization } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/thesislevel> ?level } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/ths> ?supervisor } . OPTIONAL {?resource <http://terms.library.ualberta.ca/role/thesiscommitteemember> ?committee} . OPTIONAL {?resource <http://terms.library.ualberta.ca/identifiers/hasCollection> ?collection} . }"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    datum = arrange(results)
    elastic(datum)


def collate(result, key, resource, datum):
    if key in datum[resource]:
        if key == 'dateAccepted' or key == 'dateCreated':
            try:
                datum[resource][key].append(parser.parse(result[key]['value']).isoformat('T'))
                print(parser.parse(result[key]['value']).isoformat('T'))
            except Exception as e:
                print(e, result[key]['value'])
                pass
        elif key == 'temporal':
            try:
                datum[resource][key].append(parser.parse(result[key]['value']).isoformat('T'))
                print(parser.parse(result[key]['value']).isoformat('T'))
            except Exception as e:
                print(e, result[key]['value'])
                pass
        else:
            datum[resource][key].append(result[key]['value'])
    else:
        datum[resource][key] = []
        if key == 'dateAccepted' or key == 'dateCreated':
            try:
                datum[resource][key].append(parser.parse(result[key]['value']).isoformat('T'))
                print(parser.parse(result[key]['value']).isoformat('T'))
            except Exception as e:
                print(e, result[key]['value'])
                pass

        elif key == 'temporal':
            try:
                datum[resource][key].append(parser.parse(result[key]['value']).isoformat('T'))
                print(parser.parse(result[key]['value']).isoformat('T'))
            except Exception as e:
                print(e, result[key]['value'])
                pass
        else:
            datum[resource][key].append(result[key]['value'])
    return datum


def arrange(results):
    datum = {}

    predicates = {
        "resourceType": "<http://purl.org/dc/terms/type>",
        "doi": "<http://purl.org/dc/terms/identifier>",
        "title": "<http://purl.org/dc/terms/title>",
        "contributor": "<http://purl.org/dc/terms/contributor>",
        "creator": "<http://purl.org/dc/terms/creator>",
        "spatial": "<http://purl.org/dc/terms/spatial>",
        "temporal": "<http://purl.org/dc/terms/temporal>",
        "subject": "<http://purl.org/dc/terms/subject>",
        "dateCreated": "<http://purl.org/dc/terms/created>",
        "dissertant": "<http://id.loc.gov/vocabulary/relators/dis>",
        "dateAccepted": "<http://purl.org/dc/terms/dateAccepted>",
        "department": "<http://vivoweb.org/ontology/core#AcademicDepartment>",
        "degree": "<http://purl.org/ontology/bibo/ThesisDegree>",
        "specialization": "<http://terms.library.ualberta.ca/thesis/specialization>",
        "level": "<http://terms.library.ualberta.ca/thesis/thesislevel>",
        "supervisor": "<http://id.loc.gov/vocabulary/relators/ths>",
        "committee": "<http://terms.library.ualberta.ca/role/thesiscommitteemember>",
        "collection": "<http://terms.library.ualberta.ca/identifiers/hasCollection>"
    }
    for result in results["results"]["bindings"]:
        resource = result['resource']['value']
        for key in predicates.keys():
            if key in result.keys() and result[key]['value'] is not '':
                if resource in datum:
                    datum = collate(result, key, resource, datum)
                else:
                    datum[resource] = {}
                    datum = collate(result, key, resource, datum)
        for data in datum:
            for key in datum[data].keys():
                datum[data][key] = list(set(datum[data][key]))
    
    return datum


def elastic(datum):
    actions = []
    es = Elasticsearch([{'host': '206.167.181.123', 'port': 9200}])
    try:
        es.indices.delete(index="era", ignore=[400, 404])
        es.indices.create(index="era", body=indexSettings)
    except Exception as e:
        print(e)
    for resource in datum.keys():
        entry = datum[resource]
        entry['resource'] = [resource]
        action = {
            "_index": "era",
            '_op_type': 'index',
            "_type": 'resource',
            "_id": entry['resource'],
            "_source": entry
        }

        actions.append(action)
    helpers.bulk(es, actions)
        

if __name__ == "__main__":
    main()