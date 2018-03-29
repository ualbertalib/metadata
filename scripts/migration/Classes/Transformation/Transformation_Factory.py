import re
from config import dates, dates_no_created 
from tools import PrintException
from Classes.Transformation.Transformations import Transform
from Mappings.ThesisGradDate import gradDate
from Mappings.IDs import IDs, IDs_noDesc
from Mappings.RestrictedCollections import restrictedCollections


class TransformationFactory():
    @staticmethod
    def getTransformation(triple, objectType, proxies):
        function = re.sub(r'[0-9]+', '', triple['predicate']['value'].split('/')[-1].replace('#', '').replace('-', ''))
        for grad in gradDate:
            #TODO: change graduationDate to graduationdate
            try:
                if (grad['subject'] in triple['subject']['value']) and (function == "graduationDate"):
                    return Transform().gradDate(grad, triple, objectType)
            except:
                PrintException()
        for d in dates:
            try:
                if (d['subject'] in triple['subject']['value']) and (function == "created"):
                    return Transform().createdDate(d, triple, objectType)
            except:
                PrintException()
        for ids in IDs:
            try:
                if (ids['subject'] in triple['subject']['value']) and (function == "description"):
                    return Transform().appendID(ids, triple, objectType)
            except:
                PrintException()
        for ids in IDs_noDesc:
            try:
                if (ids['subject'] in triple['subject']['value']) and (function == "modified"):
                    return Transform().appendID_noDesc(ids, triple, objectType)
            except:
                PrintException()
        for date in dates_no_created:
            try:
                if (date['subject'] in triple['subject']['value']) and (function == "title"):
                    return Transform().add_created(date, triple, objectType)
            except:
                PrintException()
        for collection in restrictedCollections:
            try:
                if (collection['subject'] in triple['subject']['value']) and (function == "restrictedCollection"):
                    return Transform().restricted(collection, triple)
            except:
                PrintException()
        if function == "created":
            try:
                return Transform().sortYear(triple, objectType)
            except:
                PrintException()
        #TODO: change graduationDate to graduationdate
        if function == "graduationDate":
            try:
                return Transform().sortYear(triple, objectType)
            except:
                PrintException()
        if function == "accessRights":
            try:
                return Transform().accessRights(triple, objectType)
            except:
                PrintException()
        elif function == "modelsmemberOf":
            try:
                return Transform().modelsmemberOf(triple, objectType)
            except:
                PrintException()
        elif function == "modelshasMember":
            try:
                return Transform().modelshasMember(triple, objectType)
            except:
                PrintException()
        elif function == "language":
            try:
                return Transform().language(triple, objectType)
            except:
                PrintException()
        elif function == "type":
            try:
                return Transform().type(triple, objectType)
            except:
                PrintException()
        elif function == "rights":
            try:
                return Transform().rights(triple, objectType)
            except:
                PrintException()
        elif function == "subject" and triple['object']['value'] != '':
            try:
                return Transform().subject(triple, objectType)
            except:
                PrintException()
                print (triple['subject']['value'], triple['object']['value'])
        elif function == "license":
            try:
                return Transform().license(triple, objectType)
            except:
                PrintException()
        elif function == "ontologyinstitution":
            try:
                return Transform().institution(triple, objectType)
            except:
                PrintException()
        elif function == "available":
            try:
                return Transform().available(triple, objectType)
            except:
                PrintException()
        elif function == "aclvisibilityAfterEmbargo":
            try:
                return Transform().aclvisibilityAfterEmbargo(triple, objectType)
            except:
                PrintException()
        elif function == "owner":
            try:
                return Transform().owner(triple, objectType)
            except:
                PrintException()
        elif ((function == "last") or (function == "first") or (function == "prev") or (function == "next") or (function == "rdfsyntaxnstype") or (function == "modelhasModel") or (function == "proxyFor") or (function == "proxyIn")) and ((objectType == 'relatedObject') or (objectType == 'technical')):
            return Transform().proxy(triple, objectType, proxies)
        else:
            return [triple]

