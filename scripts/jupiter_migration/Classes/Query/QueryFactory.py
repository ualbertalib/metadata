from Classes import Query

class queryFactory():
    @staticmethod
    def getMigrationQuery(queryHelper):
        """ returns a specified query object depending on the type passed in"""
        if queryHelper.objectType == "collection":
            return Query.Collection(queryHelper)
        elif queryHelper.objectType == "community":
            return Query.Community(queryHelper)
        elif queryHelper.objectType == "thesis":
            return Query.Thesis(queryHelper)
        elif queryHelper.objectType == "generic":
            return Query.Generic(queryHelper)
        elif queryHelper.objectType == "technical":
            return Query.Technical(queryHelper)
        elif queryHelper.objectType == "relatedObject":
            return Query.Related_Object(queryHelper)
        else:
            return None
