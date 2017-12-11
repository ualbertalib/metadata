import re
from config import dates
from tools import PrintException
from Classes.Transformation.Transformations import Transform


class TransformationFactory():
    @staticmethod
    def getTransformation(triple, objectType):
        function = re.sub(r'[0-9]+', '', triple['predicate']['value'].split('/')[-1].replace('#', '').replace('-', ''))
        for d in dates:
            try:
                if (d['subject'] in triple['subject']['value']) and (function == "created"):
                    return Transform().createdDate(d, triple, objectType)
                if (d['subject'] in triple['subject']['value']) and (function == "graduationdate"):
                    return Transform().gradDate(d, triple, objectType)
            except:
                PrintException()
        if function == "created":
            try:
                return Transform().sortYear(triple, objectType)
            except:
                PrintException()
        if function == "graduationdate":
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
        elif function == "subject":
            try:
                return Transform().subject(triple, objectType)
            except:
                PrintException()
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
        else:
            return [triple]
