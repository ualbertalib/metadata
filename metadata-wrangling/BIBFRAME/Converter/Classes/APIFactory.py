from Utils import PrintException
from Classes.SearchAPI import SearchAPI

class APIFactory():
    @staticmethod
    def get_API(name, query_type, api, log_file):
        if api == 'search_api_LC':
            try:
                return SearchAPI(name, query_type, log_file).search_api_LC()
            except:
                PrintException(log_file, name)
        if api == 'search_api_LCS':
            try:
                return SearchAPI(name, query_type, log_file).search_api_LCS()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VF':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VF()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VFP':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VFP()
            except:
                PrintException(log_file, name)
        if api == 'search_api_VFC':
            try:
                return SearchAPI(name, query_type, log_file).search_api_VFC()
            except:
                PrintException(log_file, name)
        if api == 'search_OCLC':
            try:
                return SearchAPI(name, query_type, log_file).search_OCLC()
            except:
                PrintException(log_file, name)