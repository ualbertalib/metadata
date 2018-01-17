from Classes.Query.Query_Builder import *

class QueryFactory():
    @staticmethod
    def getMigrationQuery(objectType, tripleStoreData):
        """ returns a specified query object depending on the type passed in"""
        if objectType == "collection":
            return Collection(objectType, tripleStoreData)
        elif objectType == "community":
            return Community(objectType, tripleStoreData)
        elif objectType == "thesis":
            return Thesis(objectType, tripleStoreData)
        elif objectType == "generic":
            return Generic(objectType, tripleStoreData)
        elif objectType == "technical":
            return Technical(objectType, tripleStoreData)
        elif objectType == "relatedObject":
            return Related_Object(objectType, tripleStoreData)
        else:
            return None
