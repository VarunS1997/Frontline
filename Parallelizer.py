from FileProcessing import ScopeObject

class Parallelizer:
    def __init__(self, scopeObject):
        self.__done = False
        self.__scopeObject = scopeObject

    def run(self):
        if(self.__scopeObject.get_type() not in ["FUNCTION", "LOOP"]):
            self.__done = True
            return
        elif(self.__scopeObject.get_type() != None):
