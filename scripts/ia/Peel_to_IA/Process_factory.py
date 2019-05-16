from Processing import *

class ProcessFactory():
    @staticmethod
    def getProcess(process):
        if process == "images":
            return images()
        else:
            return None
