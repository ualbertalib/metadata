from Classes.Query.QueryBuilder import *

class queryFactory():
    @staticmethod
    def getMigrationQuery(objectType, tripleStoreData, uri_generator):
        """ returns a specified query object depending on the type passed in"""
        if objectType == "collection":
            return Collection(objectType, tripleStoreData, uri_generator)
        elif objectType == "community":
            return Community(objectType, tripleStoreData, uri_generator)
        elif objectType == "thesis":
            return Thesis(objectType, tripleStoreData, uri_generator)
        elif objectType == "generic":
            return Generic(objectType, tripleStoreData, uri_generator)
        elif objectType == "technical":
            return Technical(objectType, tripleStoreData, uri_generator)
        elif objectType == "relatedObject":
            return Related_Object(objectType, tripleStoreData, uri_generator)
        else:
            return None
