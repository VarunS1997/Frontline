from ScopeObject import ScopeObject
import re

class Parallelizer:
    parForCounter = 0
    def __init__(self, scopeObject):
        self.__done = False
        self.__parallelized = False
        self.__scopeObject = scopeObject
        self.__tabCount = self.__scopeObject.get_line().count("\t")

    def run(self):
        scopeType = self.__scopeObject.get_type()
        if(scopeType != None):
            if(scopeType not in ["FUNCTION", "FORLOOP", "WHILELOOP"]):
                self.__done = True
                return
            elif(scopeType == "FORLOOP"):
                self.__prep_for_loop()
                self.__parallelize_loop()

    def __prep_for_loop(self):
        """
        Makes the for loop contain a subresult variable which will be the return value and will contain a list of tuples to call (func, args)
        """

        uniqueId = str(self.__scopeObject.get_id())
        varName = self.__scopeObject.get_line().rstrip().split(" ")[1]

        self.__scopeObject.add_child("\t"*(self.__tabCount+1) + "subresult" + uniqueId + " = []", "STATEMENT", 0)

        internalVars = self.__find_localized_variables()

        for line in self.__scopeObject:
            funcMatch = re.match(r"(?P<funcCall>(?P<func>([a-zA-Z]*\.)*[a-zA-Z]+)\((?P<args>[^+\-/*\n]*)\)[ \n])", line)
            if(funcMatch != None):
                args = funcMatch.group("args").replace(" ", "").split(",")
                if any([arg not in internalVars for arg in args]):
                    self.__scopeObject.get_child(line).replace("subresult.append(({0}, {1}))".format(funcMatch.group("func"), tuple(args)))

        loopFuncDec = "\t"*self.__tabCount
        loopFuncDec += "def PARFOR" + uniqueId + "(" + varName + "):"

        Parallelizer.parForCounter += 1

        self.__scopeObject.replace(loopFuncDec)
        self.__scopeObject.add_child("\t"*(self.__tabCount+1) + "return subresult")


    def __parallelize_for_loop(self):
        oldCode = self.__scopeObject.get_line()
        uniqueId = str(self.__scopeObject.get_id())

        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p = Pool(4)")
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "result" + uniqueId + " = p.map(PARFOR" + uniqueId + ", [" + varName + " " + oldCode.rstrip()[:-1] + "])")
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p.join()")
        self.__scopeObject.get_parent().add_child("\t"*self.__tabCount + "p.close()")

    def __find_localized_variables(self)-> list:
        """
        returns a list of variable declarations
        """
        variables = set()
        for line in self.__scopeObject:
            varMatch = re.match(r"(?P<variable>(\w)+)(\s*)=(\s*)(\w|\.|\'|\")+", line)
            if(varMatch != None):
                variables.insert(varMatch.group("variable"))
        return variables

    def __is_parallizable(self):
        '''
        Checks that the scope object is self-contained
        '''
        pass
